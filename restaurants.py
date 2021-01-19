import geopy.distance as gd  # used to calculate distances in a coordinate system
from datetime import datetime, timedelta  # import datetime and timedelta for comparison of dates


class Restaurants:
    """a class to use on returning restaurants according to coordinates and given data,
     with the restaurant being within distance specified(default 1.5km)"""
    def __init__(self, customer_coords, restaurants_list, distance=1.5):
        self.coords = customer_coords
        self.data = restaurants_list
        self.valid_restaurants = self.proper_location(distance)
        # restaurants that are in the range of distance specified

    def proper_location(self, distance):
        """return restaurants within the 1.5km radius using
        geopy.distance.distance calculation with geodesic distance"""

        return [restaurant for restaurant in self.data
                if gd.distance(self.coords, restaurant['location']).km < distance]

    def popular_restaurants(self):
        """return popular restaurants in the area, sorted by popularity"""
        return sorted(self.valid_restaurants,
                      key=lambda restaurant: (restaurant['online'], restaurant['popularity']),
                      reverse=True)

    def new_restaurants(self):
        """return new restaurants in the area, online first, sorted by launch-date ascending order"""
        # pick restaurants that are atleast 4 months or younger
        now = datetime.now()
        early_sort = [restaurant for restaurant in self.valid_restaurants if
                      (now - datetime.strptime(restaurant['launch_date'], '%Y-%m-%d')) < timedelta(days=120)]
        # sort by being online, then youngest
        return sorted(early_sort,
                      key=lambda restaurant:
                      (not restaurant['online'],
                       datetime.strptime(restaurant['launch_date'], '%Y-%m-%d')))

    def nearby_restaurants(self):
        """return nearby restaurants, online first, then nearest in ascending order"""
        return sorted(self.valid_restaurants,
                      key=lambda restaurant:
                      (not restaurant['online'],
                       gd.distance(self.coords, restaurant['location'])))

    def sections(self, amount=10):
        """returns a list of popular, new, and nearby restaurants according to the customers coordinates,
        can specify max per list, default = 10"""
        sections = []
        popular = self.popular_restaurants()[:amount]
        if len(popular) != 0:
            sections.append({'title': 'Popular Restaurants',
                             'restaurants': popular})
        new = self.new_restaurants()[:amount]
        if len(new) != 0:
            sections.append({'title': 'New Restaurants',
                             'restaurants': new})
        nearby = self.nearby_restaurants()[:amount]
        if len(nearby) != 0:
            sections.append({'title': 'Nearby Restaurants',
                             'restaurants': nearby})
        return {'sections': sections}
