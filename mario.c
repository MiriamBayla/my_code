#include <cs50.h>
#include <stdio.h>

void gap(int spaces);
void dashes(int length);

int main(void)
{
    int height = get_int("What's the height? ");

    while (!(height > 0 && height < 9))
    {
        height = get_int("What's the height? ");
    }

    if (height > 0 && height < 9)
    {
        int spaces = height - 1;
        for (int i = 0; i < height; i++)
        {
            gap(spaces);
            dashes(i + 1);
            printf("  ");
            dashes(i + 1);
            printf("\n");
            spaces--;
        }
    }
}

void gap(int spaces)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
}

void dashes(int length)
{
    for (int i = 0; i < length; i++)
    {
        printf("#");
    }
}
