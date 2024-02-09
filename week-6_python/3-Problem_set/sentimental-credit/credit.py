# TODO
from cs50 import get_string


def main():
    N = 0
    while int(N) <= 0:
        N = get_string("Number: ")

    check(N)


def valid(number):
    num_a = int(number) // 10
    num_b = int(number)
    sum = 0

    # Add the doubled numbers
    while num_a != 0:
        if ((num_a % 10) * 2 >= 10):
            sum += ((num_a % 10) * 2) // 10 + ((num_a % 10) * 2) % 10
        else:
            sum += (num_a % 10) * 2

        num_a = num_a // 100

    # Add the rest of the numbers
    while (num_b != 0):
        sum += num_b % 10
        num_b = num_b // 100

    # Check if valid
    if sum % 10 == 0:
        return True
    else:
        return False
    

def check(number):
    num = int(number)
    # Check if valid
    if valid(num) == False:
        print("INVALID")

    # Check if Amex
    elif num // 10000000000000 == 34 or num // 10000000000000 == 37:
        print("AMEX")

    # Check if mastercard
    elif num // 100000000000000 >= 51 and num // 100000000000000 <= 55:
        print("MASTERCARD")

    # Check if Visa
    elif (num // 1000000000000 >= 1 and num // 1000000000000 <= 9) or (num / 1000000000000000 >= 1 and num / 1000000000000000 <= 9):
        print("VISA")

    else:
        print("INVALID")


main()

