from heapq import heappop, heapify
from random import randint
import sys

##############
# Unchanging #
##############

common = ['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C', 'U', 'D', 'P', 'M', 'H', 'G', 'B', 'F', 'Y', 'W', 'K', 'V', 'X', 'Z', 'J', 'Q']
starting_guesses = ['ARISE', 'TASER', 'PAINT', 'SWING', 'FRAME']

####################
# Helper functions #
####################

def filter_heap(heap, guess_tuple, color_string):
    new_heap = []
    for word_tuple in heap:
        if fits_template(color_string, guess_tuple, word_tuple):
            new_heap.append(word_tuple)
    heapify(new_heap)
    return new_heap

def fits_template(color_string, guess_tuple, word_tuple):
    for i in range(5):
        # Case 1: it's green
        if color_string[i] == 'G' and word_tuple[1][i] != guess_tuple[1][i]:
            return False
        # Case 2: it's yellow
        elif color_string[i] == 'Y':
            # Must be present and not in its original spot
            if word_tuple[1].count(guess_tuple[1][i]) < 1 or cantbe[i].count(word_tuple[1][i]) > 0:
                return False
        # Case 3: it's grey
        elif color_string[i] == '-':
            # Must not be present
            if cantbe[i].count(word_tuple[1][i]) > 0:
                return False
    return True

##################
# Initialization #
##################

#guess = (-1, starting_guesses[randint(0, 4)]) # Unused weight
guess = (-1, 'TASER')
next_guess = ''
permute_list = list()           # List of letters to permute
cantbe = [[], [], [], [], []]   # List of letters at each index that were 'Y'
colorstr = ''
attempts = 1

# Generate heap (priority queue) of all words based on commonality weight
word_list = []
with open('words.txt', 'r') as file:
    for line in file:
        weight = (common.index(line[i]) + 1 for i in range(0,5))
        word_list.append((sum(weight), line[0:5]))
heapify(word_list)
        
        
################
#     Main     #
################

while attempts <= 6:
    print(guess[1])
    while len(colorstr) != 5 and colorstr != 'r':
        if len(word_list) == 0:
            print("We ran out of words? Something went wrong...")
            sys.exit()
        colorstr = input('>> ')
        if colorstr == 'r':
            if attempts != 1:
                # New solution
                guess = heappop(word_list)
                print(guess[1])
            else:
                print("You cannot reject the first solution.")
            colorstr = ''
    if colorstr == 'GGGGG':
        print("Correct! Took {} attempts".format(attempts))
        break
    for i, color in enumerate(colorstr):
        # Green: lock it in place (don't change it)
        if color == 'G':
            next_guess += 'G'
        # Yellow: add to cantbe, add to permute_list, set to '-'
        elif color == 'Y':
            permute_list.append(guess[1][i])
            cantbe[i].append(guess[1][i])
            next_guess += '-'
        # Grey: add to cantbe if not a yellow elsewhere, set to '-'
        else:
            next_guess += '-'
            # Only goes in ALL cantbes if not in permute_list
            # Else only in the current one
            if guess[1][i] not in permute_list:
                for j in range(5):
                    cantbe[j].append(guess[1][i])
            else:
                cantbe[i].append(guess[1][i])
    # Now eliminate words from heap
    print(cantbe)
    word_list = filter_heap(word_list, guess, colorstr)
    guess = heappop(word_list)
    # Re-initialize
    permute_list.clear()
    colorstr = ''
    attempts += 1

# Failure!
if attempts > 6:
    print("Failed.")
