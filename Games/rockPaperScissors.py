import sys
import getpass

def playerNameInput():   
    """
    This function prompts two users to enter their names.
    This returns the names
    """
    p1 = input("Player 1 enter your name:")
    p2 = input("Player 2 enter your name:")
    return(p1,p2)

def playerChoice(p1,p2):
    """
    This function takes in two parameters: player1 name and player2 name.
    It prompts the users to enter their choice for RPS
    This returns the players choices.
    """
    p1choice = getpass.getpass(prompt =("{name} enter your choice (r,p,s):".format(name = p1)))
    p2choice = getpass.getpass(prompt =("{name} enter your choice (r,p,s):".format(name = p2)))
    return(p1choice,p2choice)
    
def logic(p1,p2,p1c,p2c):
    """This function takes in 4 parameters: 
    player1 name, player2 name, player1 choice, player2 choice. 
    This returns a string of who wins rock paper scissors based on the players choices
    """
    pass
    # Make inputs lower case for comparissons
    p1c = p1c.lower()
    p2c = p2c.lower()
    
    if(p1c == p2c):
        return("Draw, nobody wins")
    elif(p1c ==  "r" and p2c == "p"):
        return("{name} wins!".format(name = p2))
    elif(p1c ==  "r" and p2c == "s"):
        return("{name} wins!".format(name = p1))
    elif(p1c ==  "p" and p2c == "r"):
        return("{name} wins!".format(name = p1))     
    elif(p1c ==  "p" and p2c == "s"):
        return("{name} wins!".format(name = p2))
    elif(p1c ==  "s" and p2c == "p"):
        return("{name} wins!".format(name = p1))
    elif(p1c ==  "s" and p2c == "r"):
        return("{name} wins!".format(name = p2))
    else:
        return("Something went wrong")        

p1,p2 = playerNameInput()

while(True):
    p1c,p2c = playerChoice(p1,p2)
    print(logic(p1,p2,p1c,p2c))
    
    playAgain = input("Write anyhing to play again, write 'n' to quit:")
    if(playAgain == 'n'):
        print('Thank you for playing')
        break

exit()