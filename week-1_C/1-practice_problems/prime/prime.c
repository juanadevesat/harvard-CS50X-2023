#include <cs50.h>
#include <stdio.h>

bool prime(int number);

int main(void)
{
    // Get start of range
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    // Get end of range
    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    // check if prime
    for (int i = min; i <= max; i++)
    {
        if (prime(i))
        {
            printf("%i\n", i);
        }
    }
}

bool prime(int number)
{
    // Checking 2 and 3
    if (number == 2 || number == 3)
    {
        return true;
    }
    // Checking 1 and even numbers
    if (number <= 1 || number % 2 == 0 || number % 3 == 0)
    {
        return false;
    }
    // Checking numbers between 4 and the square root of MAX
    for (int i = 5; i * i <= number; i ++)
    {
        if (number % i == 0 || number % (i + 2) == 0)
        {
            return false;
        }
    }
    return true;
}