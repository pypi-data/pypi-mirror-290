import sys
import time


# Simple typewriter-like print animation
def typewrite(text: str, delay):
    """
    Takes in a string and a delay time, and flushes a character from the string with a delay between each.

    **May lag on some IDEs and devices.**
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


# Simple typewriter-like input animation
def typewrite_inp(text: str, delay):
    """
    Takes in a string and a delay time, and flushes a character from the string with a delay between each,
    then prints a blank input statement and returns the input given.

    **May lag on some IDEs and devices.**
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    ans = input()
    return ans
