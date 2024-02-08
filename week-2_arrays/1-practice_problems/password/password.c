// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password) == true)
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    int low = 0;
    int upp = 0;
    int num = 0;
    int sym = 0;
    for (int i = 0; i < strlen(password); i++)
    {
        if (islower(password[i]))
        {
            low = 1;
        }
        else if (isupper(password[i]))
        {
            upp = 1;
        }
        else if (isdigit(password[i]))
        {
            num = 1;
        }
        else if (ispunct(password[i]))
        {
            sym = 1;
        }
    }
    if (low == 1 && upp == 1 && num == 1 && sym == 1)
    {
        return true;
    }
    else
    {
        return false;
    }

}
