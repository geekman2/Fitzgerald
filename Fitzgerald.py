import random
import itertools

locations = ["Alpha","Bravo","Charlie","Delta","Echo"]
people = ["Alfred","Becka","Chad","Dale","Emily"]
time_frames = {}
stops = []


def get_time_between(locA,locB):
    location_pair = "<>".join(sorted([locA,locB]))
    if location_pair in time_frames:
        return time_frames[location_pair]

    else:
        if location_pair[0] == location_pair[1]:
            time_frames[location_pair] = 0
            return 0
        else:
            move_time = random.randint(0,30)
            time_frames[location_pair] = move_time
            return move_time

for person in people:
    places = [(lambda x:random.choice(locations))(x) for x in range(3)]
    for ii,place in enumerate(places):
        if ii == 0:
            print ii
            home = random.choice(locations)
            stops.append(
                {person:[home,0]}
            )
            stops.append(
                {person:[places[ii],get_time_between(home,places[ii])]}
            )
        else:
#            print places[ii-1]
#            print places[ii]
            stops.append(
                {person:[places[ii-1],places[ii],get_time_between(places[ii-1],places[ii])]}
            )

print stops