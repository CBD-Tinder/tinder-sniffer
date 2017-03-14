import re
import robobrowser
import math
import numpy

EARTH_RADIUS = 6371
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"


def get_fb_access_token(email, password):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)
    f = s.get_form()
    s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
    return access_token

def get_data_to_update(profile, distance_filter=63, age_filter_max=100, age_filter_min=18):
    new_params = dict()

    if profile.distance_filter < distance_filter:
        new_params["distance_filter"] = distance_filter
        print("Changing old distance filter %s to new one %s...", profile.distance_filter, distance_filter)

    if profile.age_filter_max < age_filter_max:
        new_params["age_filter_max"] = age_filter_max
        print("Changing old max age %s to new one %s...", profile.age_filter_max, age_filter_max)

    if profile.age_filter_min > age_filter_min:
        new_params["age_filter_min"] = age_filter_min
        print("Changing old min age %s to new one %s...", profile.age_filter_min, age_filter_min)

    return new_params

def get_axis_coordinates(lat, lon):
    x = EARTH_RADIUS *(math.cos(math.radians(lat)) * math.cos(math.radians(lon)))
    y = EARTH_RADIUS *(math.cos(math.radians(lat)) * math.sin(math.radians(lon)))
    z = EARTH_RADIUS *(math.sin(math.radians(lat)))
    return x, y, z

# Full explanation of this wizardry is found on our favourite bible, the Stack project
# Pls, pray one minute if you read this to ensure it's future
# http://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-and-longitude-points-and-3-distances
def get_lat_long_trilateration(first_point, second_point, third_point):
    P1 = numpy.array(get_axis_coordinates(first_point['lat'], first_point['lon']))
    P2 = numpy.array(get_axis_coordinates(second_point['lat'], second_point['lon']))
    P3 = numpy.array(get_axis_coordinates(third_point['lat'], third_point['lon']))

    #from wikipedia
    #transform to get circle 1 at origin
    #transform to get circle 2 on x axis
    ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
    i = numpy.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
    ez = numpy.cross(ex,ey)
    d = numpy.linalg.norm(P2 - P1)
    j = numpy.dot(ey, P3 - P1)

    #from wikipedia
    #plug and chug using above values
    x = (pow(first_point['dist'],2) - pow(second_point['dist'],2) + pow(d,2))/(2*d)
    y = ((pow(first_point['dist'],2) - pow(third_point['dist'],2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

    # only one case shown here
    z = numpy.sqrt(pow(first_point['dist'],2) - pow(x,2) - pow(y,2))

    #triPt is an array with ECEF x,y,z of trilateration point
    triPt = P1 + x*ex + y*ey + z*ez

    #convert back to lat/long from ECEF
    #convert to degrees
    lat = math.degrees(math.asin(triPt[2] / EARTH_RADIUS))
    lon = math.degrees(math.atan2(triPt[1],triPt[0]))

    return lat, lon
