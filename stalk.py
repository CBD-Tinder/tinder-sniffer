import pynder
import sys
from params import *
from utils import get_data_to_update, get_bd_session, get_lat_long_trilateration
from models import init_database, User
from user_ids import ids_to_stalk

from dateutil.relativedelta import relativedelta
import datetime

############################################################################################################

def init_session(facebook_data, facebook_token, position, interested_in):
	session = pynder.Session(facebook_id=facebook_data[0], facebook_token=facebook_token)
	session.update_location(position[0], position[1])

	new_params = get_data_to_update(session.profile, distance_filter, age_filter_max, age_filter_min)
	if new_params:
	    session.update_profile(new_params)

	session.update_profile({"gender_filter": interested_in})

	return session

############################################################################################################

# Different positions around Seville
positions = {
	0: (37.393131, -6.242210),
	1: (37.549678, -5.812246),
	2: (37.196298, -5.783697),
}

genders_interested = [1, 1, 0]  # 0 = male, 1 = female

now = datetime.datetime.now()
cur_hour = now.hour

# Initialize all 3 sessions
print("Initializing Tinder sessions...", flush=True)
pos1 = positions[cur_hour % 3]
pos2 = positions[(cur_hour + 1) % 3]
pos3 = positions[(cur_hour + 2) % 3]

session1 = init_session(facebook_1, facebook_token_1, pos1, genders_interested[cur_hour % 3])
session2 = init_session(facebook_2, facebook_token_2, pos2, genders_interested[(cur_hour + 1) % 3])
session3 = init_session(facebook_3, facebook_token_3, pos3, genders_interested[(cur_hour + 2) % 3])

session1.pos = pos1
session2.pos = pos2
session3.pos = pos3

# Add the new users to stalk, if any
print("Looking for new users to stalk...", flush=True)
set_ids_to_stalk = set(ids_to_stalk)
set_ids_to_stalk.update([user.id for user in session1.nearby_users(limit=search_limit)])
set_ids_to_stalk.update([user.id for user in session2.nearby_users(limit=search_limit)])
set_ids_to_stalk.update([user.id for user in session3.nearby_users(limit=search_limit)])

print("Total: %d users to stalk." % len(set_ids_to_stalk), flush=True)

# Update the data
with open("user_ids.py", "w") as f:
	f.write("ids_to_stalk = %s\n" % str(list(set_ids_to_stalk)))

user_data = {}

# Obtain data from the users
for user_id in set_ids_to_stalk:

	try:
		data_session_1 = session1._api.user_info(user_id)
		data_session_2 = session2._api.user_info(user_id)
		data_session_3 = session3._api.user_info(user_id)
	except pynder.errors.RequestError as err:
		print("Skipping user '%s': %s" % (user_id, str(err)), flush=True)

	user = data_session_1["results"]
	user_birthdate = datetime.datetime.strptime(user["birth_date"][0:10], "%Y-%m-%d")
	user_age = relativedelta(now, user_birthdate).years

	lat, lon = get_lat_long_trilateration({'lat': session1.pos[0], 'lon': session1.pos[1], 'dist': data_session_1["results"]["distance_mi"] * 1.60934},
										  {'lat': session2.pos[0], 'lon': session2.pos[1], 'dist': data_session_2["results"]["distance_mi"] * 1.60934},
										  {'lat': session3.pos[0], 'lon': session3.pos[1], 'dist': data_session_3["results"]["distance_mi"] * 1.60934})

	user_data[user_id] = {
							'gender': 'f' if user["gender"] == 1 else 'm',
							'age': user_age,
							'lat': lat,
							'lon': lon
						 }

	if len(user_data) % 100 == 0:
		print("%d users stalked" % len(user_data), flush=True)

filename = "data/" + now.strftime("%Y%m%d_%H00.txt")
print("Writing results to " + filename, flush=True)
with open(filename, "w") as f:
	f.write(str(user_data))