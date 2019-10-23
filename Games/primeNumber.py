import sys 

def userInput():
    return int(input("Please enter a number: \n"))

def logic(number):
    if(number > 1):
        # shall only be able to divied by 1 or itself
        for n in range(2, number):
            if(number % n)==0:
                print("Number {num} is not a prime number".format( num = number))
                break
        else:
            print("Number {num} is a prime number".format( num = number))
    # exceptions when number is smaller than 1
    else:
        return("Number {num} is not a prime number".format( num = number))

logic(userInput())
exit()