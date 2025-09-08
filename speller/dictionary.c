// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 1125;

// Hash table
node *table[N];

// Global variable for words in file
int num_words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);

    // Creating a pointer at beggining of list at hashed index
    node *p = table[index];

    while (p != NULL)
    {
        if (strcasecmp(word, p->word) == 0)
        {
            return true;
        }
        p = p->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    int length = strlen(word);
    for (int i = 0; i < length; i++)
    {
        if (isalpha(word[i]))
        {
            sum += (toupper(word[i]) - 65);
        }
    }
    return sum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");

    if (source == NULL)
    {
        printf("Could not open dictionary file\n");
        return false;
    }

    // Read each word in the file
    while (fscanf(source, "%s", word) == 1)
    {
        // Changing num_words for size function
        num_words++;

        // Create node for word
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            fclose(source);
            unload();
            return false;
        }

        // Copying the word into a node
        strcpy(new_node->word, word);

        int index = hash(word);

        // Add each word to the hash table
        new_node->next = table[index];
        table[index] = new_node;
    }
    // Close the dictionary file
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // We counted each word when it was loaded from dictionary file
    return num_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *p = table[i];
            node *temp = p->next;
            while (temp != NULL)
            {
                free(p);
                p = temp;
                temp = temp->next;
            }
            free(p);
        }
    }
    return true;
}
