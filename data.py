import json  # to load the json file easily


def restaurant_json_data():
    with open('restaurants.json', 'r') as file:  # use the data from the file,
        # easy enough to change to use a server for example
        data = json.load(file)['restaurants']  # use the restaurants key to get the list
    return data
