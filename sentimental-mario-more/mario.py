from cs50 import get_int


def main():

    height = get_int("What's the height? ")

    while (not (height > 0 and height < 9)):

        height = get_int("What's the height? ")

    if (height > 0 and height < 9):
        spaces = height - 1
        for i in range(height):
            gap(spaces)
            dashes(i + 1)
            print("  ", end="")
            dashes(i + 1)
            print()
            spaces = spaces - 1


def gap(spaces):
    for i in range(spaces):
        print(" ", end="")


def dashes(length):
    for i in range(length):
        print("#", end="")


main()
