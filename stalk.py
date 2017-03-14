import pynder
import sys
from params import *
from utils import get_data_to_update, get_bd_session
from models import init_database, User

# Logging in Tinder...
session = pynder.Session(facebook_id, facebook_token)

# Checking the parameters... If one of them is outdated, we just update it
new_params = get_data_to_update(session.profile, distance_filter, age_filter_max, age_filter_min)

if len(new_params) != 0:
    session.update_profile(new_params)

db_session = get_bd_session(db_url)

print("aqui estamos hamijos")
# If there isn't new people nearby, it just launches an exception, so....
for user in session.nearby_users(limit=search_limit):
    if db_session.query(User).filter(User.id == user.id).count() == 0:
        new_user = User(id = user.id, age= user.age, gender = user.gender, name = user.name)
        db_session.add(new_user)

db_session.commit()
