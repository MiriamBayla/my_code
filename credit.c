#include <cs50.h>
#include <stdio.h>

// Function checking if number fits Luhn's algorithm
void formula(long num, int times, string type);

int main(void)
{
    int first, second, count = 2;
    long copy;
    long num = get_long("Please enter credit card number: ");
    copy = num;
    // Storing amount of digits in credit number as count while leaving first 2 digits of number
    while (copy / 100 != 0)
    {
        count++;
        copy /= 10;
    }
    // Storing the second digit in number as variable second and then deleting it
    second = copy % 10;
    copy /= 10;
    // Storing the first digit in number as variable first and then deleting it
    first = copy % 10;
    // In case of American Express number of digits and starting digits - check if fits Luhn's
    // algorithm.
    if (count == 15 && first == 3 && second == 4)
    {
        formula(num, 15, "AMEX\n");
    }
    else if (count == 15 && first == 3 && second == 7)
    {
        formula(num, 15, "AMEX\n");
    }
    // In case of Visa number of digits and starting digits - check if fits Luhn's algorithm.
    else if (count == 13 && first == 4)
    {
        formula(num, 13, "VISA\n");
    }
    else if (count == 16 && first == 4)
    {
        formula(num, 16, "VISA\n");
    }
    // In case of Mastercard number of digits and starting digits - check if fits Luhn's algorithm.
    else if (count == 16 && first == 5 && second > 0 && second < 6)
    {
        formula(num, 16, "MASTERCARD\n");
    }
    // If number of digits or starting digits don't match those of Amex, Visa or Mastercard print
    // INVALID.
    else
    {
        printf("INVALID\n");
    }
}

// Function checking if number fits Luhn's algorithm
void formula(long num, int times, string type)
{
    long copy = num;
    int add, jumps = 1, sum = 0;
    // Go through all digits in credit number
    for (int i = 0; i < times; i++)
    {
        // Add every other digit starting from last place to sum
        if (jumps == 1)
        {
            sum += copy % 10;
            copy /= 10;
            jumps = 2;
        }
        // Multiply every other digit starting by second to last by 2 and add the digits of that
        // product to sum
        if (jumps == 2)
        {
            add = copy % 10 * 2;
            sum += add % 10;
            add /= 10;
            sum += add % 10;
            copy /= 10;
            jumps = 1;
        }
    }
    // If sum's last digit is 0 - this is a valid credit card number and the credit card company's
    // name will be printed.
    if (sum % 10 == 0)
    {
        printf("%s", type);
    }
    // If sum's last digit is not 0 - this is not a valid credit card number and INVALID will be
    // printed.
    else
    {
        printf("INVALID\n");
    }
}
