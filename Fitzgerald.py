import pandas as pd
import random
from itertools import permutations

locations = ["Alpha","Bravo","Charlie","Delta","Echo"]
people = ["Alfred","Becka","Chad","Dale","Emily"]


def get_time_between(locA,locB):
    first_location,second_location = (locA,locB).sort()
    if first_location == second_location:
        return 0
    else:
        return random.randint(0,30)



print time_frame["LocationA"].LocationB


