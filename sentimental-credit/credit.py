from cs50 import get_int, get_string


def main():

    count = 2
    num = get_int("Please enter credit card number: ")
    copy = num
    # Storing amount of digits in credit number as count while leaving first 2 digits of number
    while (int(copy / 100) != 0):
        count += 1
        copy //= 10

    # Storing the second digit in number as variable second and then deleting it
    second = copy % 10
    copy //= 10

    # Storing the first digit in number as variable first and then deleting it
    first = copy % 10

    # In case of American Express number of digits and starting digits - check if fits Luhn's
    # algorithm.
    if count == 15 and first == 3 and second == 4:
        formula(num, 15, "AMEX")

    elif count == 15 and first == 3 and second == 7:
        formula(num, 15, "AMEX")

    # In case of Visa number of digits and starting digits - check if fits Luhn's algorithm.
    elif count == 13 and first == 4:
        formula(num, 13, "VISA")

    elif count == 16 and first == 4:
        formula(num, 16, "VISA")

    # In case of Mastercard number of digits and starting digits - check if fits Luhn's algorithm.
    elif count == 16 and first == 5 and second > 0 and second < 6:
        formula(num, 16, "MASTERCARD")

    # If number of digits or starting digits don't match those of Amex, Visa or Mastercard print
    # INVALID.
    else:
        print("INVALID")


# Function checking if number fits Luhn's algorithm
def formula(num, times, type):
    copy = num
    jumps = 1
    sum = 0
    # Go through all digits in credit number
    for i in range(times):
        # Add every other digit starting from last place to sum
        if jumps == 1:
            sum += copy % 10
            copy //= 10
            jumps = 2

        # Multiply every other digit starting by second to last by 2 and add the digits of that
        # product to sum
        if jumps == 2:
            add = copy % 10 * 2
            sum += add % 10
            add //= 10
            sum += add % 10
            copy //= 10
            jumps = 1

    # If sum's last digit is 0 - this is a valid credit card number and the credit card company's
    # name will be printed.
    if sum % 10 == 0:
        print(type)

    # If sum's last digit is not 0 - this is not a valid credit card number and INVALID will be
    # printed.
    else:
        print("INVALID")


main()
