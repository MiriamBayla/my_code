#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int numLetters(string text);
int numWords(string text);
int numSentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letters = numLetters(text);
    int words = numWords(text);
    int sentences = numSentences(text);

    // Compute the Coleman-Liau index
    float avgLetters = (float) letters / words * 100;
    float avgSentences = (float) sentences / words * 100;
    float gradeLevel = 0.0588 * avgLetters - 0.296 * avgSentences - 15.8;
    int grade = round(gradeLevel);

    // Print the grade level
    if (grade == 16 || grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

// Return the number of letters in text
int numLetters(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

// Return the number of words in text
int numWords(string text)
{
    int count = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 32)
        {
            count++;
        }
    }
    return count;
}

// Return the number of sentences in text
int numSentences(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 46 || text[i] == 63 || text[i] == 33)
        {
            count++;
        }
    }
    return count;
}
