import sys
import random

def logic(guess,number):
    """ This function takes in two numbers and compares the guess to the number and returns a string based on if the guess is
    Correct, Lower or Higher
    """
    if(guess == number):
        return("Correct")
    elif(guess > number):
        return("Lower")
    elif(guess < number):
        return("Higher")

number = random.randint(0,10)
i = 0
while(True):
    i += 1
    guess = int(input("Guess my number? (between 0-10) \n"))
    print(logic(guess,number))
    
    if(guess == number):
        print("It took you {times} to guess my number".format(times = i))
        if(input("Write 'y' to Exit \n") == 'y'):
            print("Thanks for playing")
            break
        i = 0
        number = random.randint(0,10)
        
exit()