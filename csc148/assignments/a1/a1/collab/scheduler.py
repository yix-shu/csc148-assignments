"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import Callable, Dict, List
from random import choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


def _capable_trucks(parcel: Parcel, trucks: List[Truck]) -> list:
    """
    Returns the list of indices of the trucks that have enough
    volume/capacity to carry the parcel.
    """
    capables = []
    for truck in trucks:
        if parcel.volume <= (truck.capacity - truck.absolute_fullness()):
            capables.append(trucks.index(truck))
    return capables


class RandomScheduler(Scheduler):
    """
    Random Scheduler organizes parcel delivery randomly
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """
        Picks a random Parcel from <parcels> and a random Truck from all the
        Trucks that have space to pack the Parcel in <trucks>, then packs it.
        If no Truck can fit a Parcel, that Parcel is added to a list which is
        returned once all the Parcels have been packed or added to this list.
        """
        parcels2 = parcels[:]
        rejects = []
        while len(parcels2) != 0:
            p = choice(parcels2)
            truck_indices = _capable_trucks(p, trucks)
            if len(truck_indices) == 0:
                rejects.append(p)
            else:
                trucks[choice(truck_indices)].pack(p)
            parcels2.remove(p)
        return rejects


def _smaller_volume(p1: Parcel, p2: Parcel) -> bool:
    """
    Returns True if p1 is smaller than p2. Returns False if not.
    """
    return p1.volume < p2.volume


def _larger_volume(p1: Parcel, p2: Parcel) -> bool:
    """
    Returns True if p1 is larger than p2. Returns False if not.
    """
    return p1.volume > p2.volume


def _larger_city(p1: Parcel, p2: Parcel) -> bool:
    """
    Returns True if Parcel <p1>'s destination is alphabetically before
    Parcel <p2>'s destination. False otherwise.
    """
    return p1.destination < p2.destination


def _smaller_city(p1: Parcel, p2: Parcel) -> bool:
    """
    Returns True if Parcel <p1>'s destination is alphabetically after
    Parcel <p2>'s destination. False otherwise.
    """
    return p1.destination > p2.destination


def _more_truck_space(t1: Truck, t2: Truck) -> bool:
    """
    Returns True if Truck <t1> has more truck space. False otherwise.
    """
    return (t1.capacity - t1.absolute_fullness()) > \
           (t2.capacity - t2.absolute_fullness())


def _less_truck_space(t1: Truck, t2: Truck) -> bool:
    """
    Returns True if Truck <t1> has less truck space. False otherwise.
    """
    return (t1.capacity - t1.absolute_fullness()) < \
           (t2.capacity - t2.absolute_fullness())


def _greedy_capable_trucks(parcel: Parcel, trucks: List[Truck]) -> list:
    """
    Returns the list of indices of the trucks that have enough
    volume/capacity to carry the parcel.
    """
    capables = _capable_trucks(parcel, trucks)
    capables2 = []
    for i in capables:
        if parcel.destination == trucks[i].route[-1]:
            capables2.append(i)
    if len(capables2) == 0:
        return capables
    return capables2


class GreedyScheduler(Scheduler):
    """
    GreedyScheduler organizes routes and parcel delivery by t_priority or
    p_priority

    ===Private Attributes===
    config: the dictionary that is inputted with all the information
    GreedyScheduler must take to do its operations

    _t_priority: the method by which we will assess truck priority

    _p_priority: the method by which we will assess parcel priority with
    _p_type.

    _p_type: whether it is volume or city that we must sort by _p_priority.

    _func: the function needed to complete the method we will sort the
    PriorityQueue of the parcels with
    """
    config: Dict
    _t_priority: str
    _p_priority: str
    _p_type: str
    _func: Callable

    def __init__(self, config: Dict) -> None:
        """
        Initializes a GreedyScheduler object using the information inputted
        in config for the schedule method.
        """
        self._p_type = config['parcel_priority']
        self._p_priority = config['parcel_order']
        self._t_priority = config['truck_order']
        if self._p_type == 'volume':
            if self._p_priority == 'non-decreasing':
                self._func = _smaller_volume
            else:
                self._func = _larger_volume
        else:
            if self._p_priority == 'non-increasing':
                self._func = _smaller_city
            else:
                self._func = _larger_city

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        rejects = []
        parcels2 = PriorityQueue(self._func)
        for p in parcels:
            parcels2.add(p)

        while not parcels2.is_empty():
            parcel = parcels2.remove()
            truckos = _greedy_capable_trucks(parcel, trucks)
            if self._t_priority == 'non-increasing':
                ordereds = PriorityQueue(_more_truck_space)
            else:
                ordereds = PriorityQueue(_less_truck_space)

            for i in truckos:
                ordereds.add(trucks[i])

            if ordereds.is_empty():
                rejects.append(parcel)
                continue

            picked = ordereds.remove()
            for t in trucks:
                if picked.id == t.id:
                    t.pack(parcel)
        return rejects


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
