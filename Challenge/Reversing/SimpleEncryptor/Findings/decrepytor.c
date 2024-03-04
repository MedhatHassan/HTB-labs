#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    FILE *fp = fopen("SimpleEncryptor/rev_simpleencryptor/flag.enc", "rb");

    if (fp != NULL)
    {
        fseek(fp, 0, SEEK_END);
        long size = ftell(fp);
        rewind(fp);

        char *fileContents = malloc(size);

        if (fileContents != NULL)
        {
            fread(fileContents, sizeof(char), size, fp);

            for (int i = 0; i < size; i++)
            {
                printf("%02X", fileContents[i]);
            }
            printf("\n\n");

            int seed;
            memcpy(&seed, fileContents, sizeof(seed));
            printf("Seed: %d\n", seed);

            srand(seed);
            int iVar1, iVar2;

            for (int i = 4; i < size; i++)
            {
                iVar1 = rand();
                iVar2 = rand() & 7;

                printf("current byte: %02X\n", fileContents[i]);
                printf("right shift: %d\n", iVar2);
                printf("XOR key: %d\n", iVar1);

                fileContents[i] = ((unsigned char)fileContents[i] >> (iVar2)) | ((fileContents[i]) << (8 - iVar2));
                printf("byte after rotate right: %02X\n", fileContents[i]);

                fileContents[i] = iVar1 ^ fileContents[i];
                printf("byte after full decryption: %02X\n", fileContents[i]);
            }

            for (int i = 4; i < size; i++)
            {
                printf("%c", fileContents[i]);
            }
        }

        free(fileContents);
        fclose(fp);
    }

    return 0;
}
