# -------------------------------------------------------------------------------
# Name:        'wordListGen'
# Purpose:     'Generate a list of 3000 random words of the specified type
# author =     'Geekman2'
# Created:     '6/22/2015'
#-------------------------------------------------------------------------------
from nltk.corpus import wordnet
import random
import pickle
import os

def wordlistGen(type_="a"):
    words = list(wordnet.all_synsets(type_))
    word_strs = []
    random.shuffle(words)
    for word in words[:1000]:
        word = str(word.lemma_names()[0])
        print word
        word_strs.append(str(word))
    pickle.dump(word_strs, open(os.getcwd()+"/"+type_+".p", "wb"))

wordlistGen("a")
wordlistGen("n")
