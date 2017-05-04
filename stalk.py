import pynder
import sys
from params import *
from utils import get_data_to_update, get_bd_session, get_lat_long_trilateration
from models import init_database, User

import datetime

############################################################################################################

def get_nearby_users_data(facebook_id, facebook_token, position):
	# Logging in Tinder...
	session = pynder.Session(facebook_id=facebook_id, facebook_token=facebook_token)
	#session.update_location(position[0], position[1])

	# Checking the parameters... If one of them is outdated, we just update it
	new_params = get_data_to_update(session.profile, distance_filter, age_filter_max, age_filter_min)

	if len(new_params) != 0:
	    session.update_profile(new_params)

	# If there isn't new people nearby, it just launches an exception, so....
	return session.nearby_users(limit=search_limit)

############################################################################################################

# Different positions around Seville
positions = {
	0: (37.393131, -6.242210),
	1: (37.549678, -5.812246),
	2: (37.196298, -5.783697),
}

# The current hour serves to make the bots switch positions and trigger Tinder updates.
now = datetime.datetime.now()
cur_hour = now.hour
n = 0
user_data = {}

print("Starting data collection...", flush=True)

# Iterate for all 3 bots and add the gathered user information
for account, token in [(facebook_1, facebook_token_1), (facebook_2, facebook_token_2), (facebook_3, facebook_token_3)]:
	acc_id = account[0]
	bot_position = positions[(cur_hour + n) % 3]
	iteration_data = get_nearby_users_data(acc_id, token, bot_position)

	for user in iteration_data:
		if user.id not in user_data:
			# If the user is not registered in this iteration, add it to the dict
			user_data[user.id] = {'name': user.name, 'age': user.age, 'gender': user.gender, 
							      'distances': [{'lat': bot_position[0], 'lon': bot_position[1], 'dist': user.distance_km}]}
		else:
			# If it already has been visited, add the new distance
			user_data[user.id]['distances'].append((bot_position, user.distance_km))

	n += 1
	print("Data collection done for bot #%d" % n, flush=True)

# Get the users whose position can be triangulated, that is, have been visited by all 3 bots
triangulable_users = [user_id for user_id in user_data if len(user_data[user_id]['distances']) == 3]
user_positions = {}

for user_id in triangulable_users:
	user = user_data[user_id]
	distances = user['distances']
	lat, lon = get_lat_long_trilateration({'lat': distances[0]['lat'], 'lon': distances[0]['lon'], 'dist': distances[0]['dist']},
										  {'lat': distances[1]['lat'], 'lon': distances[1]['lon'], 'dist': distances[1]['dist']},
										  {'lat': distances[2]['lat'], 'lon': distances[2]['lon'], 'dist': distances[2]['dist']})

	user_positions[user_id] = {'name': user["name"], 'age': user["age"], 'gender': user["gender"], 'lat': lat, 'lon': lon}

filename = now.strftime("%Y%m%d_%H00.txt")
with open(filename, "w") as f:
	f.write(str(user_positions))
