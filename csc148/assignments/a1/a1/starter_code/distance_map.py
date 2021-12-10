"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """ A "map" containing distances from one city to another.

    ===== Private Attributes =====
    _distances:
      Dictionary containing tuples containing two cities as a key, and
      the distance between them as values.
    """
    _distances: Dict

    def __init__(self) -> None:
        """Create an empty DistanceMap, with no cities and no distances.

        >>> m = DistanceMap()
        >>> m.is_empty()
        True
        """
        self._distances = {}

    def add_distance(self, a: str, b: str, ab: int, ba: int = None) -> None:
        """Adds to the DistanceMap the distance between two cities <a> and <b>,
        as well as the distance between <b> and <a>. If <ba> is <None>,
        then <ab> is assumed equal to <ba>.

        >>> m = DistanceMap()
        >>> m.add_distance("Toronto", "Markham", 30)
        >>> m.distance("Toronto", "Markham")
        30
        >>> m.distance("Markham", "Toronto")
        30
        >>> m.add_distance("Etobicoke", "Guelph", 80, 75)
        >>> m.distance("Etobicoke", "Guelph")
        80
        >>> m.distance("Guelph", "Etobicoke")
        75
        """
        # Make a new entry into the dictionary for the distance a -> b
        self._distances[(a, b)] = ab
        # If ba is given, then make a new entry into the dictionary for
        # the distance from b -> a
        if ba is not None:
            self._distances[(b, a)] = ba
        # Otherwise, distance b -> a equals a -> b.
        else:
            self._distances[(b, a)] = ab

    def distance(self, a: str, b: str) -> int:
        """Given two different cities <a> and <b>, if the distance
        between them is in the dictionary, return that distance as
        an int. Otherwise, return -1.

        >>> m2 = DistanceMap()
        >>> m2.add_distance("Barrie", "Oakville", 125)
        >>> m2.distance("Barrie", "Oakville")
        125
        >>> m2.add_distance("Ottawa", "Kingston", 196)
        >>> m2.distance("Oshawa", "Kingston")
        -1
        """
        # Check if distance from a -> b is in DistanceMap
        if (a, b) in self._distances:
            return self._distances[(a, b)]
        # If it's not, then return -1
        return -1

    def is_empty(self) -> bool:
        """Returns whether DistanceMap has information stored in it.

        >>> m3 = DistanceMap()
        >>> m3.is_empty()
        True
        >>> m3.add_distance("London", "Oshawa", 239)
        >>> m3.is_empty()
        False
        """
        return not bool(self._distances)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
