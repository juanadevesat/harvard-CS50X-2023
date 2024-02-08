#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Get card number from user
    long num = 0;
    do
    {
        num = get_long("Credit card number: ");
    }
    while (num < 0);

    long num_a = num;
    long num_b = num;

    //Add alternate digits and multiply by 2
    num_a = num_a / 10;
    int sum = 0;
    while (num_a != 0)
    {
        if ((num_a % 10) * 2 >= 10)
        {
            sum += ((num_a % 10) * 2) / 10 + ((num_a % 10) * 2) % 10;
        }
        else
        {
            sum += (num_a % 10) * 2;
        }

        num_a = num_a / 100;
    }

    //Add the rest of the numbers
    while (num_b != 0)
    {
        sum += num_b % 10;
        num_b = num_b / 100;
    }

    //Check if valid
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        //Check if Amex
        if (num / 10000000000000 == 34 || num / 10000000000000 == 37)
        {
            printf("AMEX\n");
        }
        //Check if mastercard
        else if (num / 100000000000000 >= 51 && num / 100000000000000 <= 55)
        {
            printf("MASTERCARD\n");
        }
        //Check if Visa
        else if ((num / 1000000000000 >= 1 && num / 1000000000000 <= 9)
                 || (num / 1000000000000000 >= 1 && num / 1000000000000000 <= 9))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

}