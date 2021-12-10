"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from csc148.assignments.a1.a1.collab.distance_map import DistanceMap


class Parcel:
    """A package that needs to be delivered.

    ===== Public Attributes =====
    id:
      A unique integer associated with the Parcel.
    volume:
      The volume of the Parcel.
    origin:
      A string that represents the name of the city that the Parcel came from.
    destination:
      A string that represents the name of the city the Parcel needs to be
      delivered to.
    """
    id: int
    volume: int
    origin: str
    destination: str

    def __init__(self, id_num: int, volume: int, o: str, d: str) -> None:
        """Create a Parcel with id <id_num>, volume <volume>, origin <o>,
        and destination <d>.

        >>> p = Parcel(1, 5, "Toronto", "Markham")
        >>> p.id == 1
        True
        >>> p.volume == 5
        True
        >>> p.origin == "Toronto"
        True
        >>> p.destination == "Markham"
        True
        """
        self.id = id_num
        self.volume = volume
        self.origin = o
        self.destination = d


class Truck:
    """ A truck that can carry Parcels.

    ===== Public Attributes =====
    id:
      A unique integer associated with each Truck.
    capacity:
      The maximum volume that the empty Truck can carry.
    depot:
      The city that the Truck starts at, and returns to.
    cargo:
      A list of all Parcels in the Truck.
    route:
      A list that describes the Truck's route. First element in the list is
      the Truck's depot.
    """
    id: int
    capacity: int
    depot: str
    cargo: list
    route: list

    def __init__(self, id_number: int, capacity: int, depot: str) -> None:
        """Create an empty Truck, meaning no Parcels in cargo, with id
        <id_number> and maximum volume capacity <capacity>. The Truck's
        depot is <depot>, and its route consists of solely the depot.

        >>> t = Truck(12, 100, "Toronto")
        >>> t.fullness() == 0.00
        True
        """
        self.id = id_number
        self.capacity = capacity
        self.depot = depot
        self.cargo = []
        self.route = [depot]

    def pack(self, package: Parcel) -> bool:
        """If there is available space greater than or equal to
        the volume of Parcel <package> in the Truck, add <package>
        to cargo, and if the package's destination is not the last one on
        the route already, add its destination to the Truck's route, then
        return True. Otherwise, return False.

        >>> t = Truck(67, 100, "Toronto")
        >>> p = Parcel(14, 80, "Toronto", "Barrie")
        >>> t.pack(p)
        True
        >>> t.cargo == [p]
        True
        >>> t.route == ["Toronto", "Barrie"]
        True
        >>> p2 = Parcel(16, 50, "Toronto", "Barrie")
        >>> t.pack(p2)
        False
        >>> t.cargo == [p, p2]
        False
        """
        # Check whether the Truck has space for the package
        if self.capacity - self.absolute_fullness() >= package.volume:
            # If it does, add it to cargo and return True
            self.cargo.append(package)
            # If the package's destination is not last on the route, add it
            if package.destination != self.route[-1]:
                self.route.append(package.destination)
            return True
        # Otherwise, return False
        return False

    def fullness(self) -> float:
        """Return how full the Truck is as a percentage.

        >>> t = Truck(26, 40, "Toronto")
        >>> p = Parcel(14, 8, "Barrie", "Toronto")
        >>> t.pack(p)
        True
        >>> t.fullness()
        20.0
        >>> p2 = Parcel(15, 12, "Barrie", "Toronto")
        >>> t.pack(p2)
        True
        >>> t.fullness()
        50.0
        """
        current_volume = 0
        for c in self.cargo:
            current_volume += c.volume
        return (current_volume / self.capacity) * 100

    def absolute_fullness(self) -> int:
        """Return the amount of used space in the Truck. This value
        is equal to the total volume of all the Parcels in cargo.

        >>> t = Truck(123, 10, "Toronto")
        >>> p = Parcel(21, 3, "Toronto", "Oakville")
        >>> t.pack(p)
        True
        >>> t.absolute_fullness()
        3
        >>> p2 = Parcel(22, 7, "Toronto", "Oakville")
        >>> t.pack(p2)
        True
        >>> t.absolute_fullness()
        10
        """
        used = 0
        for p in self.cargo:
            used += p.volume
        return used


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        return f"There are {len(self.trucks)} trucks in this fleet."

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        num = 0
        for t in self.trucks:
            if not t.fullness() == 0:
                num += 1
        return num

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        allocations = {}
        for t in self.trucks:
            parcels = []
            for p in t.cargo:
                parcels.append(p.id)
            allocations[t.id] = parcels
        return allocations

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        # <cap> is used to find total capacity of non-empty trucks, and
        # <used> is used to find total used volume of non-empty trucks
        cap = 0
        used = 0
        for t in self.trucks:
            # Check if the Truck is non-empty
            if not t.fullness == 0.0:
                # If it is non-empty, modify variables as needed
                cap += t.capacity
                used += t.absolute_fullness()
        # Return the difference between total capacity and used space
        return cap - used

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        tot_full = 0.00
        for t in self.trucks:
            # Check if the Truck is non-empty
            if not t.fullness == 0.0:
                # If it is, add its fullness to tot_full
                tot_full += t.fullness()
        # Return the sum of all the fullness of the trucks
        return tot_full

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        # _total_fullness() already accounts for only non-empty trucks
        return self._total_fullness() / self.num_nonempty_trucks()

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        one_way = 0
        back = 0
        # Check each Truck
        for t in self.trucks:
            # If there is only one item in the route, then the Truck does not
            # travel, and thus we add nothing
            if len(t.route) == 1:
                one_way += 0
                back += 0
            # Otherwise, make a new list of tuples that contains each
            # consecutive pair of destinations in route, and add each distance
            else:
                for pair in zip(t.route, t.route[1:]):
                    one_way += dmap.distance(pair[0], pair[1])
                back += dmap.distance(t.route[-1], t.route[0])
        # Return the distance travelled by each Truck on their route, plus
        # the distance from each Truck's last destination to the depot.
        return one_way + back

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        travelled = 0
        for t in self.trucks:
            # Check whether a Truck has travelled a non-zero distance
            if len(t.route) != 1:
                travelled += 1
        # Return the total travelled distance divided by the number of trucks
        # that have travelled a non-zero distance
        return self.total_distance_travelled(dmap) / travelled


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
