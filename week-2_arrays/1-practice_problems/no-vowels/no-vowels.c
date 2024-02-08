// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>

string replace(string word);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./no-vowels word\n");
    }
    else
    {
        printf("%s\n", replace(argv[1]));
    }
}

string replace(string word)
{
    string w = word;
    for (int x = 0; x < strlen(word); x++)
    {
        switch (word[x])
        {
            case 'a':
                w[x] = '6';
                break;
            case 'e':
                w[x] = '3';
                break;
            case 'i':
                w[x] = '1';
                break;
            case 'o':
                w[x] = '0';
                break;
        }
    }
    return w;
}
