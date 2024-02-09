#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    // TODO
    int num;

    char unit_digit = input[strlen(input) - 1] - 48;

    string new_input = input;

    if (strlen(new_input) == 0)
    {
        return 0;
    }
    else
    {
        new_input[strlen(input) - 1] = '\0';
        num = unit_digit + (10 * convert(new_input));
    }

    return num;
}