import numpy
from random import randint
# Generate array
str_array = numpy.ndarray(shape=(26, 26, 26, 26, 26), dtype=numpy.ubyte, order='C')
with open('words.txt', 'r') as file:
    for line in file:
        ints = list((ord(line[i]) - 65 for i in range(0,5)))
        str_array[ints[0]][ints[1]][ints[2]][ints[3]][ints[4]] = 1   

# Now do the guessing
common = ['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C', 'U', 'D', 'P', 'M', 'H', 'G', 'B', 'F', 'Y', 'W', 'K', 'V', 'X', 'Z', 'J', 'Q']
cantbe = [[], [], [], [], []]

def generate_perms(guess_string, permute_list, solutions):
    if len(permute_list) == 0:
        solutions.append(guess_string.copy())
        return
    i = 0
    while i < 5:
        if guess_string[i] != '-':
            i += 1
        else:
            if cantbe[i].count(permute_list[0]) > 0:
                # This letter can't be here since it must be permutted
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
                    # This letter can't be here since it must be permutted
                    j += 1
                    continue
                guess_string[i] = letter_list[j] # Most common letter
                generate_guess(guess_string, letter_list, solution)
                # Next iteration
                guess_string[i] = '-'
                j += 1
            # We shouldn't get here, so return
            return
    
    

starting_guesses = ['ARISE', 'TASER', 'PAINT', 'SWING', 'FRAME']
guess = list((char for char in starting_guesses[randint(0, 4)]))
guess_int = list(ord(char) - 65 for char in guess)
next_guess = ['-', '-', '-', '-', '-']
permute_list = list()
colorstr = ''
guess_letters = common
attempts = 1

while attempts <= 6:
    print(guess)
    # Remove guess from array
    str_array[guess_int[0]][guess_int[1]][guess_int[2]][guess_int[3]][guess_int[4]] = 0
    while len(colorstr) != 5:
        colorstr = input('>> ')
    if colorstr == 'GGGGG':
        print("Correct! Took {} attempts".format(attempts))
        break
    for i, color in enumerate(colorstr):
        # If it's green, lock it in place (don't change it!)
        if color == 'G':
            next_guess[i] = guess[i]
        # If it's yellow, add to list to permute and set to -1
        # Add this letter to the list where it can't be.
        elif color == 'Y':
            permute_list.append(guess[i])
            cantbe[i].append(guess[i])
            next_guess[i] = '-'
        # If grey, remove from letters to guess set to -1
        else:
            next_guess[i] = '-'
            if guess_letters.count(guess[i]) != 0:
                guess_letters.remove(guess[i])
    # Get permutation strings only if there is at least one.
    permstring_list = list()
    if len(permute_list) > 0:
        generate_perms(next_guess, permute_list, permstring_list)
    else:
        permstring_list.append(next_guess)
    # Now do actual guesses with filling in letters
    solution_list = list()
    for string in permstring_list:
        generate_guess(string, guess_letters, solution_list)
    # Get which one is most common (lowest value)
    lowest_value = 200
    lowest_string = []
    for string in solution_list:
        value = 0
        for val in string:
            value += string.index(val)
        if value < lowest_value:
            lowest_value = value
            lowest_string = string
    # Set next guess to lowest
    guess = lowest_string
    # Reset lists
    permute_list.clear()
    permstring_list.clear()
    solution_list.clear()
    colorstr = ''
    attempts += 1
# Down here we failed
if attempts > 6:
    print("Failed.")
