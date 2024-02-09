#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("How to use use: $ ./reverse inputname.wav outputname.wav\n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER header;
    fread(&header, 1, 44, input);

    // Use check_format to ensure WAV format
    // TODO #4
    if (check_format(header) == 0)
    {
        printf("The file is not a WAV file\n");
    }

    // Open output file for writing
    // TODO #5
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Write header to file
    // TODO #6
    fwrite(&header, 1, 44, output);

    // Use get_block_size to calculate size of block
    // TODO #7
    int block_size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    uint8_t buffer[block_size];

    //move pointer to end of input and set pointer back 1 audio blocks
    fseek(input, -block_size, SEEK_END);

    while (ftell(input) > 44)
    {
        //read 1 audio block into buffer
        fread(&buffer, block_size, 1, input);

        //write buffer into output
        fwrite(&buffer, block_size, 1, output);

        // set pointer back 2 audio blocks
        fseek(input, -2 * block_size, SEEK_CUR);
    }
    //while loop ends before the first audio block in input is passed into output, therefore:
    //read first audio block into buffer and write buffer into last audio block of output
    fread(&buffer, block_size, 1, input);
    fwrite(&buffer, block_size, 1, output);

    // Close files
    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 1;
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    // number of channels multiplied by bytes per sample
    int size = header.numChannels * header.bitsPerSample / 8;

    return size;
}