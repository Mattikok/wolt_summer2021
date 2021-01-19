import flask  # create a simple discovery Api using Flask for python
import json  # json to load the data file to memory
from flask import abort, jsonify, request  # imports to use
import restaurants as rt  # import helper class

app = flask.Flask('WoltSummerJob')  # set name to be package name for easier debugging
app.config['DEBUG'] = True  # set to debug mode for better developing
app.config['JSON_SORT_KEYS'] = False  # set to not sort dictionarys with jsonify
# since it would mess up the order defined in restaurants.py

with open('restaurants.json', 'r') as file:  # use the data from the file,
    # easy enough to change to use a server for example
    data = json.load(file)['restaurants']  # use the restaurants key to get the list


# required data loaded, configure api next

@app.route('/discovery', methods=['GET'])
def discovery():
    if 'lat' and 'lon' in request.args:  # check that latitude and longitude are given
        try:
            latitude = float(request.args['lat'])
            longitude = float(request.args['lon'])
        except ValueError:
            abort(400, description='Check latitude and longitude')
            return
    else:  # abort if not specified
        abort(404, description="Missing arguments lat or lon")
        return

    # use the restaurants class for actual handling of data, pass it the restaurants available and coordinates
    restaurants = rt.restaurants((longitude, latitude), data)

    # finally change to proper format using jsonify
    return jsonify(restaurants.sections())


# run the application after configuration is done
app.run()
