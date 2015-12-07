#-------------------------------------------------------------------------------
# Name:        'Horace'
# Purpose:     'Genetica algorithm multiple body coordination'
# author =     'Geekman2'
# Created:     '12/2/2015'
#-------------------------------------------------------------------------------
import random
import operator
import pickle

locations = pickle.load(open("locations.p", "rb"))
checked_location_pairs = pickle.load(open("checked.p", "rb"))
departing_from = pickle.load(open("departing_from.p", "rb"))

def individual():
    """Individual is route, which is random in length
     and uses a random assortment of locations and people
     going to them"""
    length = random.randint(0,10)
