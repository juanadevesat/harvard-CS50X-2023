#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;

FILE *image;
char photo_name[8];
int photo_number = 0;

int main(int argc, char *argv[])
{
    // Check for impropper usage:
    if (argc != 2)
    {
        printf("Usage: $ ./recover image.raw");
        return 1;
    }

    // Open image and check if it was opened correctly:
    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        printf("Could not open file");
        return 1;
    }

    // Write data from image into a jpg:
    BYTE buffer[BLOCK_SIZE];

    while (fread(&buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close previous photo except if starting
            if (photo_number > 0)
            {
                fclose(image);
            }

            // Open a new empty JPEG with the next name
            sprintf(photo_name, "%0*i.jpg", 3, photo_number);
            image = fopen(photo_name, "w");
            photo_number++;
        }

        if (photo_number > 0)
        {
            fwrite(&buffer, 1, BLOCK_SIZE, image);
        }
    }

    fclose(image);
    fclose(raw_file);
}