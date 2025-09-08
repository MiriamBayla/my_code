#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void convert(string text, char argv1[]);

int main(int argc, string argv[])
{
    // Error message if no key or more than one key entered
    if (argv[2] != 0 || argv[1] == 0)
    {
        printf("Error: Use one key. \n");
        return 1;
    }

    // Error messages if key is invalid
    int count = 0;

    // Defining an array that will store a switch for each letter. Making every place 0.
    char arr[26];
    for (int j = 0; j < 26; j++)
    {
        arr[j] = 0;
    }

    // Going through each letter in key checking for errors
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        // Error if a character in the key is not part of the alphabet
        if (!isalpha(argv[1][i]))
        {
            printf("Error: Only enter alphabetical characters. \n");
            return 1;
        }

        // Printing error if letter already exists
        if (arr[toupper(argv[1][i]) - 65] == 1)
        {
            printf("Error: No duplicates allowed in key. \n");
            return 1;
        }
        else
        {
            arr[toupper(argv[1][i]) - 65] = 1;
        }

        // Adding the amount of letters in the key
        count++;
    }

    // Error if key does not have 26 letters
    if (count != 26)
    {
        printf("Error: Key must be 26 characters. \n");
        return 1;
    }

    // Asking the user for text
    string text = get_string("Plaintext: ");

    // Printing the text in ciphertext
    printf("ciphertext: ");
    convert(text, argv[1]);
    return 0;
}

// Converting text into ciphertext
void convert(string text, char argv1[])
{
    char newTxt[strlen(text)];
    for (int i = 0; i < strlen(text); i++)
    {
        // If a character is not a letter - keep that character
        if (!isalpha(text[i]))
        {
            newTxt[i] = text[i];
        }
        else if (islower(text[i]))
        {
            newTxt[i] = tolower(argv1[text[i] - 97]);
        }
        else
        {
            newTxt[i] = toupper(argv1[text[i] - 65]);
        }
    }
    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c", newTxt[i]);
    }
    printf("\n");
}
