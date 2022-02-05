import numpy
from random import randint

###########
# Globals #
###########

common = ['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C', 'U', 'D', 'P', 'M', 'H', 'G', 'B', 'F', 'Y', 'W', 'K', 'V', 'X', 'Z', 'J', 'Q']
starting_guesses = ['ARISE', 'TASER', 'PAINT', 'SWING', 'FRAME']

####################
# Helper functions #
####################

def generate_perms(guess_string, permute_list, solutions):
    """ Generates permuted strings using the 'Y' characters """
    if len(permute_list) == 0:
        solutions.append(guess_string.copy())
        return
    i = 0
    while i < 5:
        if guess_string[i] != '-':
            i += 1
        else:
            if cantbe[i].count(permute_list[0]) > 0:
                # This letter can't be here since it must be permuted
                i += 1
                continue
            guess_string[i] = permute_list[0]
            permute_list = permute_list[1:]
            # Recursive call to place rest of permute list
            generate_perms(guess_string, permute_list, solutions)
            # Add back to the list
            permute_list.insert(0, guess_string[i])
            guess_string[i] = '-'
            i += 1
            
def generate_guess(guess_string, letter_list, solution):
    """ Generates solution strings using the rest of guess_letters """
    if guess_string.count('-') == 0:
        # Check if the solution exists in str_array
        ints = list(ord(char) - 65 for char in guess_string)
        if (str_array[ints[0]][ints[1]][ints[2]][ints[3]][ints[4]].tolist()) == 1:
            solution.append(guess_string.copy())
            return
    i = 0
    while i < 5:
        if guess_string[i] != '-':
            i += 1
        else:
            j = 0
            while j < len(letter_list):
                if cantbe[i].count(letter_list[j]) > 0:
                    # This letter can't be here since it must be permuted
                    j += 1
                    continue
                #print("j = {}".format(j))
                guess_string[i] = letter_list[j] # Most common first
                generate_guess(guess_string, letter_list, solution)
                guess_string[i] = '-' # Exhausted recursive guesses
                j += 1
            i += 1 # Exhausted solutions

##################
# Initialization #
##################

guess = list((char for char in starting_guesses[randint(0, 4)]))
guess_int = list(ord(char) - 65 for char in guess)
next_guess = ['-', '-', '-', '-', '-']
permute_list = list()           # List of letters to permute
permstring_list = list()        # List of strings with permuted letters
solution_list = list()          # List of candidate solutions
cantbe = [[], [], [], [], []]   # List of letters at each index that were 'Y'
colorstr = ''
guess_letters = common          # Initialize with all 26 letters
attempts = 1

# Generate 5-dimensional row-major array of words (will be sparsely populated)
# Saves time compared to a BFS or DFS
str_array = numpy.ndarray(shape=(26, 26, 26, 26, 26), dtype=numpy.ubyte, order='C')
with open('words.txt', 'r') as file:
    for line in file:
        ints = list((ord(line[i]) - 65 for i in range(0,5)))
        str_array[ints[0]][ints[1]][ints[2]][ints[3]][ints[4]] = 1
        
################
#     Main     #
################

while attempts <= 6:
    str_guess = "".join(guess)
    print(str_guess)
    # Remove guess from array
    str_array[guess_int[0]][guess_int[1]][guess_int[2]][guess_int[3]][guess_int[4]] = 0
    while len(colorstr) != 5:
        colorstr = input('>> ')
    if colorstr == 'GGGGG':
        print("Correct! Took {} attempts".format(attempts))
        break
    for i, color in enumerate(colorstr):
        # Green: lock it in place (don't change it)
        if color == 'G':
            next_guess[i] = guess[i]
        # Yellow: add to cantbe, add to permute_list, set to '-'
        elif color == 'Y':
            permute_list.append(guess[i])
            cantbe[i].append(guess[i])
            next_guess[i] = '-'
        # Grey: remove from letters to guess, set to '-'
        else:
            next_guess[i] = '-'
            if guess_letters.count(guess[i]) != 0:
                guess_letters.remove(guess[i])
    # Only get permstrings if there's at least one letter to permute
    if len(permute_list) > 0:
        generate_perms(next_guess, permute_list, permstring_list)
    else:
        permstring_list.append(next_guess)
    # Generate solutions
    for string in permstring_list:
        generate_guess(string, guess_letters, solution_list)
    lowest_value = 130 # Lowest value = most common
    lowest_string = []
    for string in solution_list:
        value = 0
        for val in string:
            value += string.index(val)
        if value < lowest_value:
            lowest_value = value
            lowest_string = string
    guess = lowest_string # Set next guess to lowest
    # Re-initialize
    permute_list.clear()
    permstring_list.clear()
    solution_list.clear()
    colorstr = ''
    attempts += 1

# Failure!
if attempts > 6:
    print("Failed.")
