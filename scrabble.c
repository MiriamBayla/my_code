#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// How many points each letter is worth
int Points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int Score(string word);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int score1 = Score(word1);
    int score2 = Score(word2);

    // Prints which player is winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int Score(string word)
{
    int score = 0;
    // Adding the scoring of every letter to the overall word's score
    for (int i = 0, length = strlen(word); i < length; i++)
    {
        if (isupper(word[i]))
        {
            score += Points[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += Points[word[i] - 'a'];
        }
    }

    return score;
}
