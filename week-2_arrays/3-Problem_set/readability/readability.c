#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// Take imput from user (text:) in main

// Function to count letters in text
int count_letters(string text);

// Function to count words
int count_words(string text);

// Function to count sentences
int count_sentences(string text);

// Function for Coleman Liau index
int index(int words, int letters, int sentences);

// Function for Coleman Liau index = 0.0588 * L - 0.296 * S - 15.8
//      where L = letters per 100 words   and   S = sentences per 100 words

//Print output in main: "Grade X" where x=1-16, "Grade 16+" or "Before Grade 1"
int main(void)
{
    string text = get_string("Text: ");
    int w = count_words(text);
    float l = count_letters(text) * 100.0 / w;
    float s = count_sentences(text) * 100.0 / w;
    int index = round((0.0588 * l) - (0.296 * s) - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) index);
    }
}

int count_letters(string text)                           // Function to count letters in text
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if isalpha(text[i])
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)                            // Function to count words
{
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if isspace(text[i])
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)                        // Function to count sentences
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}



