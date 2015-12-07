# -------------------------------------------------------------------------------
# Name:        ''
# Purpose:
# author =     'Geekman2'
# Created:     '7/20/2015'
# -------------------------------------------------------------------------------
import pickle
import itertools
import random
import cProfile
import time

import googlemaps
import requests

requests.packages.urllib3.disable_warnings()
locations = pickle.load(open("locations.p", "rb"))
checked_location_pairs = pickle.load(open("checked.p", "rb"))
departing_from = pickle.load(open("departing_from.p", "rb"))
destinations = []
people = []
fail_count = 0
start = time.clock()


class Person:
    def __init__(self,
                 name,
                 home,
                 driver=False,
                 location=None):
        self.name = name
        self.home = home
        self.driver = driver
        if location is None:
            self.location = home


class Car:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.in_car = []

    def pickup(self, person):
        self.in_car.append(person)

    def goto(self, location):
        self.location = location

    def dropoff(self, person):
        self.in_car.remove(person)
        person.location = self.location


class Place:
    def __init__(self,
                 name,
                 address,
                 rendevous=False):
        self.name = name
        self.address = address
        self.rendevous = rendevous
        self.at = {}
        obj = {"name": name, "address": address, "rendevous": rendevous}
        locations.append(obj)
        departing_from[self.address] = {}
        pickle.dump(locations, open("locations.p", "wb"))
        pickle.dump(departing_from, open("departing_from.p", "wb"))
        calculate_times()


def time_between(origin, destination):
    """

    :type destination: Location
    """
    location_pair = tuple(sorted((origin, destination)))
    if location_pair in checked_location_pairs:
        return checked_location_pairs[location_pair]
    else:
        gmaps = googlemaps.Client(key="AIzaSyBH611O9hTPbO1CJmIoF2ReBeTZ5WlI0B0")
        distance = gmaps.distance_matrix(origin,
                                         destination,
                                         )
        text = distance["rows"][0]["elements"][0]["duration"]["text"]
        value = distance["rows"][0]["elements"][0]["duration"]["value"]
        minutes = text[0:text.find("m") - 1]
        try:
            departing_from[origin][destination] = minutes
        except KeyError:
            departing_from[origin] = {}
            departing_from[origin][destination] = minutes
        try:
            departing_from[destination][origin] = minutes
        except KeyError:
            departing_from[destination] = {}
            departing_from[destination][origin] = minutes
        return minutes



def calculate_times():
    for pair in itertools.combinations(locations, 2):
        first = pair[0]
        second = pair[1]
        first_name = first["name"]
        second_name = second["name"]
        first_address = first["address"]
        second_address = second["address"]
        tog = tuple(sorted((first_address, second_address)))

        if tog in checked_location_pairs:
            pass
            # print "Already checked", first_name, "and", second_name
        else:
            print(first_name, "and", second_name, time_between(first_address, second_address), "minutes")
            checked_location_pairs[tog] = time_between(first_address, second_address)
    pickle.dump(checked_location_pairs, open("checked.p", "wb"))

def route_check(route):
    global fail_count
    fail = False
    for dest in destinations:
        #TODO Remove name from dest
        if not any(d['to'] == dest["name"] for d in route):
            fail = True
            break
    if fail == False:
        return True
    else:
        fail_count+=1
        return False

def generate_potentials():
    potential_routes = []
    for person in people:
        """"The purpose of this code segment is to generate a set of possible routes for each person in our group"""
        potentials = []
        perms = []
        for i in range(3,len(destinations)+1):
            perms.append(itertools.permutations(destinations,i))
        for permutations in perms:
            for route in permutations:
                if route[0]["address"] == person.location:
                    route_times = []
                    totime = 0
                    zipped = zip(route,route[1:])
                    for pair in zipped:
                        totime += int(time_between(pair[0]["address"],pair[1]["address"]))
                        #TODO put full location object in route, removed for debugging
                        route_times.append({"from":pair[0]["name"],"to":pair[1]["name"],"tim_of_arrival":totime,"Who":[person.name]})
                    potentials.append({"route":route_times,"total_time":totime})
                    person.best = sorted(potentials,
                                         key=lambda x:x["total_time"])
                else:
                    pass
    for person_pair in itertools.combinations(people,2):
        """This segment is designed to compare and combine the routes of each possible pair of people in our group.
        First we use itertools.product to generate all possible pairs out of each persons list of routes.
        After checking if the routes are identical (which should be impossible) it uses a pair of nested iterators
        to check every possible combination of locations. It checks to see if the location and arrival times are
        identical, if they are, it then creates two possible routes, both are identical until the point of
        intersection, at which point one continues along the first persons path, and the other continues along the
        second path."""
        person1 = person_pair[0]
        person2 = person_pair[1]
        product = itertools.product(person1.best,person2.best)
        for route_pair in product:
            if route_pair[0]["route"] == route_pair[1]["route"]:
                print "Routes are identical"
                pass
            else:
                route1 = route_pair[0]["route"]
                route2 = route_pair[1]["route"]
                for loc1 in route1:
                    for loc2 in route2:
                        time_difference = abs(loc1["time_of_arrival"] - loc2["time_of_arrival"])
                        if time_difference < 5 and loc1["to"] == loc2["to"]:
                            person1_intersection = route1.index(loc1)
                            person2_intersection = route2.index(loc2)
                            for i in route1[person1_intersection:]:
                                if person2.name not in i["Who"]:
                                    i["Who"].append(person2.name)
                            for it in route2[person2_intersection:]:
                                if person1.name not in it["Who"]:
                                    it["Who"].append(person1.name)
                            potential_route1 = route1+route2[:person2_intersection-1]
                            potential_route2 = route1[:person1_intersection-1]+route2
                            potential_route1.sort(key=lambda x:x["time_of_arrival"])
                            potential_route2.sort(key=lambda x:x["time_of_arrival"])
                            if route_check(potential_route1) == True:
                                potential_routes.append(potential_route1)
                            if route_check(potential_route2) == True:
                                potential_routes.append(potential_route2)

    return potential_routes


if __name__ == "__main__":
    calculate_times()
    for i in range(7):
        rand = random.choice(locations)
        while rand in destinations:
            rand = random.choice(locations)
        destinations.append(rand)

    home1 = random.choice(destinations)["address"]
    home2 = random.choice(destinations)["address"]

    people.append(Person(name="Alice",driver=True,home = home1))
    people.append(Person(name="Bob",driver=True,home = home2))

    potential_routes = generate_potentials()
    print len(potential_routes)
    print  (time.clock()-start)/60
    #cProfile.run("generate_potentials()")







