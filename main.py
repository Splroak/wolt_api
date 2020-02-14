# -*- coding: utf-8 -*-
import json
from geopy import distance
from urllib.parse import urlparse
from urllib.parse import parse_qs

with open('restaurants.json') as data:
    json_output = json.load(data)
# List of all restaurant
restaurant_list = []

# List of restaurant returned by the search
valid_restaurant = []

# JSON file to return
json_return = []

# Parse the search query URL
search_query = urlparse('/restaurants/search?q=sushi&lat=60.17045&lon=24.93147')

# Extract 'q' parameter from the parsed URL
q_param = parse_qs(search_query.query)['q']

# Extract 'lat' parameter from the parsed URL
lat_param = float(parse_qs(search_query.query)['lat'][0])

# Extract 'lon' parameter from the parsed URL
lon_param = float(parse_qs(search_query.query)['lon'][0])


def generate_api(query,latitude,longitude):
    for i in range(len(json_output['restaurants'])):
        # Name of the restaurants
        name = json_output['restaurants'][i]['name']
    
        # Description of the restaurants
        description = json_output['restaurants'][i]['description']
    
        # Longitude of the restaurants
        lon = json_output['restaurants'][i]['location'][0]
    
        # Latitude of the restaurants
        lat = json_output['restaurants'][i]['location'][1]
    
        # List of keywords to search for for each restaurant
        keyword_list = ''
        keyword_list += ' ' + name
        keyword_list += ' ' + description
        for j in json_output['restaurants'][i]['tags']:
            keyword_list += ' ' + j
    
        # Id, keywords, longitude and latitude of a restaurant
        restaurant = {'ID':i,
                  'keywords':keyword_list,
                  'longitude':lon,
                  'latitude':lat}
    
        # Append everything into a big list of restaurants
        restaurant_list.append(restaurant)

    # Coordinate of the user
    user_coord = (latitude,longitude)
    
    # Iterate through the restaurant list, if a keyword (partially) match
    # the search, retrieve that restaurant's longitude and latitude,
    # then calculate the distance between user's device and the restaurant
    # in kilometers. If the distance is smaller than 3, append that restaurant
    # to the valid restaurant list.
    for res in restaurant_list:
        if query[0] in res['keywords']:
            res_coord = (res['latitude'],res['longitude'])

            travel_distance = distance.distance(user_coord,res_coord).km
            if travel_distance <= 3:
                valid_restaurant.append(res)

    # If there's no nearby restaurant, print no result.      
    if len(valid_restaurant) == 0:
        print('No result.')
    
    for res in valid_restaurant:
        json_return.append(json_output['restaurants'][res['ID']])
    
    # write valid_restaurants to a json file
    with open('valid_restaurants.json','w') as data:
        json.dump(json_return,data)

generate_api(q_param,lat_param,lon_param)