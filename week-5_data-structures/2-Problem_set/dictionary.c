// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 456977;

// Hash table
node *table[N];

int dictionary_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node *n = table[hash(word)];

    while (n != NULL)
    {
        if (strcasecmp(word, n -> word) == 0)
        {
            return true;
        }
        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hashvalue = 0;

    if (word[1] == '\0' || word[2] == '\0' || word[3] == '\0')
    {
        hashvalue = (toupper(word[0]) - 'A') * 26;
    }
    else
    {
        hashvalue = (toupper(word[0]) - 'A') * 26 * 26 * 26 + (toupper(word[1]) - 'A') * 26 * 26 + (toupper(word[2]) - 'A') * 26 +
                    (toupper(word[3]) - 'A');
    }
    return hashvalue;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dict = fopen(dictionary, "r");
    if (dictionary == NULL)
    {
        return false;
    }

    char nextword[LENGTH + 1];

    while (fscanf(dict, "%s", nextword) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n -> word, nextword);

        int hashvalue = hash(nextword);

        n -> next = table[hashvalue];
        table[hashvalue] = n;

        dictionary_size ++;
    }

    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        while (n != NULL)
        {
            node *tmp = n;
            n = n -> next;
            free(tmp);
        }
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
