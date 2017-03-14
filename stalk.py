import pynder
import sys
from params import *
from utils import get_data_to_update

# Logging in Tinder...
session = pynder.Session(facebook_id, facebook_token)

# Checking the parameters... If one of them is outdated, we just update it
new_params = get_data_to_update(session.profile, distance_filter, age_filter_max, age_filter_min)

if len(new_params) != 0:
    session.update_profile(new_params)

try:
    # If there isn't new people nearby, it just launches an exception, so....
    for user in session.nearby_users(limit=search_limit):
        print("Name: ", user.name, " Fecha de Nacimiento:", user.birth_date)
except:
    print("No people found bro...")
