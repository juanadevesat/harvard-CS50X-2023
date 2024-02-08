#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height from user
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // print piramid
    for (int i = 1; i <= height; i++)
    {
        // print buffer (empty spaces)
        for (int j = height - i; j > 0 ; j--)
        {
            printf("%c", ' ');
        }
        // print first half of piramid
        for (int j = 0 ; j < i; j++)
        {
            printf("%c", '#');
        }
        // print gap
        printf("  ");
        // print second half of piramid
        for (int j = 0 ; j < i; j++)
        {
            printf("%c", '#');
        }
        printf("\n");
    }


}