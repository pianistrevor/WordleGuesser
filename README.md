# Wordle Guesser
## Version: 1.1

I've fallen victim to the viral craze of the online game [Wordle](https://www.powerlanguage.co.uk/wordle/).
It's a game much like Mastermind, but instead of six colors, there's 26 letters.
I'm a quick solver (I've gotten every one since 2022-01-28 in 5 tries or less so far), but I wanted to see if a computer could solve it more quickly.

I've switched the roles, so that YOU get to enter the "correctness" of the word, and the *computer* will guess the next word.
Basic usage is as follows:
- Make sure you have numpy installed. If you don't, run `pip install numpy` to install it.
- Running `python guesser.py` will start the game, and the computer will output the first guess (a list of 5 characters)
- You enter a 5-character color string based on whether each character is '-' (not in the list), 'Y' (in the list but not in the correct spot), or 'G' (in the list and in the correct spot).
- The computer will then generate another guess, and this process repeats until success ('GGGGG') or failure (> 6 attempts).
*Note that if the computer's guess has two of the same letter, both out of place, only one letter gets a 'Y'.*

The internal constraint on the attempts is posed by Wordle and can be easily changed.
If you want to suggest any updates or think this can or should be improved, just let me know. I'm happy to maintain this.

## Changelog:
### Version 1.1 (2022-02-06):
* Add ability to reject a solution (if Wordle doesn't recognize it)
* Fix generate_guess() to prevent infinite loops
* Refactor solution selection code for performance
* Add numpy requirement to README.md
### Version 1.0 (2022-02-04):
* Initial release.