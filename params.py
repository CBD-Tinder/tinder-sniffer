import os
from utils import get_fb_access_token

# Authentication parameters
facebook_id         = os.environ["facebook_id"]
facebook_password   = os.environ["facebook_password"]
facebook_token      = get_fb_access_token(facebook_id, facebook_password)

# Search parameters
distance_filter     = 63    # 100 km in miles... Those retard-units though
age_filter_max      = 100   # Gerontophilia is allowed. Nechrophilia... Nope
age_filter_min      = 18    # We don't want to visit the jail, right?
search_limit        = 100   # Amount of people we look for in every tinderization
photo_size          = 640   # Width of the retrieved photos

# Database Params
db_url = "sqlite:///tarkinder.db"
