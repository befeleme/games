from random import randint
from pathlib import Path
import string

word_list = ["woman", "computer", "pyladies", "python"]

def load_pic(death_count):
    "Finds a path to picture with the state of game the same as the death_count"
    if death_count < 10:
        my_file = "0" + str(death_count) + ".txt"
    else: 
        my_file = str(death_count) + ".txt" 
    p = Path('obesenec/').joinpath(my_file)
    return p
        
def evaluate_letter(chosen_word, chosen_string, death_count):
    "Evaluates what the player guesses and returns both string and current death_count"
    guess = "A" # starting state, just to enter while loop 
    while True:
        if guess not in string.ascii_lowercase:  # input control
            guess = input("Choose a letter (just small one!): ") # ask for his guess
        elif guess in chosen_word: # Changes _ to letter.
            c = chosen_word.index(guess)
            chosen_string = chosen_string[:c] + guess + chosen_string[c+1:]   
            return chosen_string, death_count    
            
        else:  # Adds unsuccessful try and load a picture of a hangman.
            death_count += 1
            print("Oh, crap. Not present in the word. Mistake no {}.".format(death_count))
            p = load_pic(death_count)
            with p.open(encoding="utf-8") as f:
                contents = f.read()     
            print(contents)
            return chosen_string, death_count

def evaluate_field(chosen_string, death_count):
    "Evaluates the state of game"
    if "_" not in chosen_string:
        return "good_end"
    elif death_count == 10:
        return "bad_end"
    else:
        return "continue"
               
# Game itself: creates a starting state
my_death_count = 0 # Starting state of mistakes
my_chosen_word = word_list[randint(0, len(word_list) -1)]   
my_chosen_string = "_" * len(my_chosen_word)
print(my_chosen_string) # Prints the hidden word
  
while True:
    if evaluate_field(my_chosen_string, my_death_count) != "continue":
        break
    my_chosen_string, my_death_count = evaluate_letter(my_chosen_word, my_chosen_string, my_death_count)
    print(my_chosen_string)
        
if evaluate_field(my_chosen_string, my_death_count) == "good_end":   
    print("You won, that is good!")
else: 
    print("Sorry, you lost.")
