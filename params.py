import os
from utils import get_fb_access_token

print("Authenticating facebook accounts...", flush=True)
# Authentication parameters
facebook_1       = (os.environ["facebook_id_1"], os.environ["facebook_password_1"])
facebook_token_1 = get_fb_access_token(facebook_1[0], facebook_1[1])
facebook_2       = (os.environ["facebook_id_2"], os.environ["facebook_password_2"])
facebook_token_2 = get_fb_access_token(facebook_2[0], facebook_2[1])
facebook_3       = (os.environ["facebook_id_3"], os.environ["facebook_password_3"])
facebook_token_3 = get_fb_access_token(facebook_3[0], facebook_3[1])

# Search parameters
distance_filter     = 31    # 50 km in miles... Those retard-units though
age_filter_max      = 100   # Gerontophilia is allowed. Nechrophilia... Nope
age_filter_min      = 18    # We don't want to visit the jail, right?
search_limit        = 1000  # Amount of people we look for in every tinderization
photo_size          = 640   # Width of the retrieved photos

# Database Params
db_url = "sqlite:///tarkinder.db"
