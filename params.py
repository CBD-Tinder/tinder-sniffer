import os
from utils import get_fb_access_token

def safe_environ(env_var):
    try:
        return os.environ[env_var]
    except KeyError:
        raise KeyError(env_var + " was not found in your system. Please, add it to the environment variables.")

# Authentication parameters
facebook_id     = safe_environ("facebook_id")
facebook_password = safe_environ("facebook_password")
facebook_token  = get_fb_access_token(facebook_id, facebook_password)

# Search parameters
distance_filter     = 63    # 100 km in miles... Those retard-units though
age_filter_max      = 100   # Gerontophilia is allowed. Nechrophilia... Nope
age_filter_min      = 18    # We don't want to visit the jail, right?
search_limit        = 100   # Amount of people we look for in every tinderization
