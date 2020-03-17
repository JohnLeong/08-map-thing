from math import *

class Coords():
    def __init__(self, lattitude = 0, longitude = 0):
        self.lattitude = lattitude
        self.longitude = longitude

    def distance_from(self, other):
        """Gets the distance from this Coord to another Coord in terms of lattitude and longitude length

        Parameters:
        other(Coords) :    The other Coord
        """
        return sqrt((self.lattitude - other.lattitude) ** 2, (self.longitude - other.longitude) ** 2)

    def distance_from_sqr(self, other):
        """Gets the distance squared from this Coord to another Coord in terms of lattitude and longitude length
        Use this instead of distance_from to save the sqrt calculation cost

        Parameters:
        other(Coords) :    The other Coord
        """
        return ((self.lattitude - other.lattitude) ** 2, (self.longitude - other.longitude) ** 2)

    ## TODO: Implement function, calculate real life distance
    def real_distance_from(self, other):
        """Gets the distance from this Coord to another Coord in terms of meters

        Parameters:
        other(Coords) :    The other Coord
        """
        #TEMP
        return 1.0
