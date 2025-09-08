#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Counter for number of jpg file
    int counter = 0;

    // Accept a single command line argument
    if (argc != 2)
    {
        printf("Correct usage - one command line. \n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    // Let user know if can't open card
    if (card == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    FILE *image = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (image != NULL)
            {
                fclose(image);
            }
            char filename[8];

            // Create JPEGs from the data
            sprintf(filename, "%03i.jpg", counter);
            image = fopen(filename, "w");
            if (image == NULL)
            {
                printf("Could not open file %s\n", filename);
                return 1;
            }
            counter++;
        }
        if (image != NULL)
        {
            fwrite(buffer, 1, 512, image);
        }
    }
    fclose(image);
    fclose(card);
}
