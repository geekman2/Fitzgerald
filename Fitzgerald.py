import random
import itertools
import pandas as pd
from matplotlib import pyplot as plt

locations = ["1234 Alpha Lane", " 456 Bravo Street", " 2345 Charlie Avenue",
             "4567 Delta Place", "795 Echo Drive"]  # Sample Locations

people = ["Alfred", "Becka", "Chad", "Dale", "Emily"]  # Sample People
time_frames = {}
stops = []

#TODO Refactor out test code

def get_time_between(locA, locB):
    """
    :param locA:First Location:String
    :param locB: Second Location:String
    :return: Time between locations:Integer
    Current Purpose: Assign random time intervals to location pairs, then store them
    if the pair has already been used, return that number

    Eventual Purpose: Query an API for time interval values
    """

    location_pair = "<>".join(sorted([locA, locB]))  # Sort the pair so that A>B doesn't get duplicated with B>A
    if location_pair in time_frames:  # Make sure we haven't done this before
        return time_frames[location_pair]

    else:
        if location_pair[0] == location_pair[1]:  # If the arrival point is the same as the destination, return time = 0
            time_frames[location_pair] = 0
            return 0
        else:
            move_time = random.randint(0, 30)  # otherwise, return a random time
            time_frames[location_pair] = move_time
            return move_time


def generate_test_cases():
    for person in people:
        current_time = 0
        place_indexes = [(lambda x: random.randint(0, len(locations) - 1))(x) for x in range(3)]
        for ii, place in enumerate(place_indexes):
            arrive_at = current_time + random.randint(1, 5)
            leave_after = arrive_at + random.randint(1, 5)
            current_time = leave_after
            if ii == 0:
                home = random.randint(0, len(locations) - 1)
                stops.append(
                    {"Name": person,
                     "from": home,
                     "to": place_indexes[ii],
                     "due": arrive_at,
                     "leave": leave_after,
                     }
                )
            else:
                stops.append(
                    {"Name": person,
                     "from": place_indexes[ii - 1],
                     "to": place_indexes[ii],
                     "due": arrive_at,
                     "leave": leave_after,
                     }
                )

stops_dataframe = pd.DataFrame(stops)


def plot_route():
    for pers in people:
        personal_stops = stops_dataframe.loc[stops_dataframe["Name"] == pers]
        times = sorted(list(personal_stops["due"]) + list(personal_stops["leave"]))
        places = [val for val in personal_stops["from"] for _ in (0, 1)]
        plt.plot(times, places, linewidth=10)

    plt.xticks(range(0, 40))
    plt.yticks(range(len(locations)), locations)
    plt.margins(0.1, axis="y")
    plt.tight_layout()

    plt.show()


def route_builder():
    order = random.shuffle(list[stops_dataframe["from"]])


