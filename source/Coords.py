import math as math

class Coords():
    def __init__(self, lattitude = 0, longitude = 0):
        self.lattitude = lattitude
        self.longitude = longitude

    def distance_from(self, other):
        """Gets the distance from this Coord to another Coord in terms of lattitude and longitude length

        Parameters:
        other(Coords) :    The other Coord
        """
        return math.sqrt((self.lattitude - other.lattitude) ** 2, (self.longitude - other.longitude) ** 2)

    def distance_from_sqr(self, other):
        """Gets the distance squared from this Coord to another Coord in terms of lattitude and longitude length
        Use this instead of distance_from to save the sqrt calculation cost

        Parameters:
        other(Coords) :    The other Coord
        """
        return ((self.lattitude - other.lattitude) ** 2 + (self.longitude - other.longitude) ** 2)

    def real_distance_from(self, other):
        """Gets the distance from this Coord to another Coord in terms of meters

        Parameters:
        other(Coords) :    The other Coord
        """
        R = 6373.0 #radius of earth
        lat1 = math.radians(self.lattitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.lattitude)
        lon2 = math.radians(other.longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
