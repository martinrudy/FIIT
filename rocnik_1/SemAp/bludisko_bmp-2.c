#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma pack(push, 1)
struct BitmapFileHeader {
  unsigned short bfType;
  unsigned int bfSize;
  unsigned short bfReserved1;
  unsigned short bfReserved2;
  unsigned int bfOffBits;
};
#pragma pack(pop)

struct BitmapInfoHeader {
  unsigned int biSize;
  int biWidth;
  int biHeight;
  unsigned short biPlanes;
  unsigned short biBitCount;
  unsigned int biCompression;
  unsigned int biSizeImage;
  int int biXPelsPerMeter;
  int int biYPelsPerMeter;
  unsigned int biClrUsed;
  unsigned int biClrImportant;
};

void write_head(FILE *f, int width, int height)
{
  if (width % 4 != 0 || height % 4 != 0)
  {
    printf("Chyba: Vyska a sirka nie su delitelne 4.\n");
    return;
  }
  struct BitmapInfoHeader bih;
  bih.biSize = sizeof(struct BitmapInfoHeader);
  bih.biWidth = width;
  bih.biHeight = height;
  bih.biSizeImage = bih.biWidth * bih.biHeight * 3;
  bih.biPlanes = 1;
  bih.biBitCount = 24;
  bih.biCompression = 0;
  bih.biXPelsPerMeter = 0;
  bih.biYPelsPerMeter = 0;
  bih.biClrUsed = 0;
  bih.biClrImportant = 0;

  struct BitmapFileHeader bfh;
  bfh.bfType = 0x4D42;
  bfh.bfSize = sizeof(struct BitmapFileHeader) + sizeof(struct BitmapInfoHeader) + bih.biSizeImage;
  bfh.bfReserved1 = 0;
  bfh.bfReserved2 = 0;
  bfh.bfOffBits = sizeof(struct BitmapFileHeader) + bih.biSize;

  fwrite(&bfh, sizeof(struct BitmapFileHeader), 1, f);
  fwrite(&bih, sizeof(struct BitmapInfoHeader), 1, f);
}

void write_pixel(FILE *f, unsigned char r, unsigned char g, unsigned char b)
{
  fwrite(&r, 1, 1, f);
  fwrite(&g, 1, 1, f);
  fwrite(&b, 1, 1, f);
}

// ukazkove kreslenie BMP obrazku
void obrazok(char *nazov_suboru)
{
	FILE *f = fopen(nazov_suboru, "wb");
	int w = sirka * 4, h = vyska * 4;
	write_head(f, w, h);

	int x, y;
	for (y = 0; y < h; y++)
		for (x = 0; x < w; x++) {
			if (riesenie[(h - 1 - y) / 4][x / 4] == 1)
				write_pixel(f, 255, 0, 0);
			else if (bludisko[(h - 1 - y) / 4][x / 4] == 1)
				write_pixel(f, 0, 0, 255);
			else
				write_pixel(f, 0, 255, 0);
		}

	fclose(f);
}

int rozmer;
int n = 0;
int bludisko[201][201];

int riesenie[201][201];


void vypisblud(int rozmer)
{
	int i, j;
	for (i = 0; i < rozmer; i++)
	{
		for (j = 0; j < rozmer; j++)
		{
			printf("%d\t", riesenie[i][j]);
		}
		printf("\n\n");
	}
}


int riesblud(int r, int c)
{

	if ((r == rozmer - 1) && (c == rozmer - 2))
	{
		riesenie[r][c] = 1;
		return 1;
	}

	if (r >= 0 && c >= 0 && r < rozmer && c < rozmer && riesenie[r][c] == 0 && bludisko[r][c] == 0)
	{

		riesenie[r][c] = 1;
		if (riesblud(r + 1, c))
			return 1;
		if (riesblud(r, c + 1))
			return 1;
		if (riesblud(r - 1, c))
			return 1;
		if (riesblud(r, c - 1))
			return 1;
		riesenie[r][c] = 0;
		return 0;
	}
	return 0;

}

int main()
{
	int i, j, n;

	while (scanf("%s", bludisko[n]) > 0) {
		n++;
	}
	rozmer = n;

	for (i = 0; i < rozmer; i++)
	{
		for (j = 0; j < rozmer; j++)
		{
			riesenie[i][j] = 0;
		}
	}
	if (riesblud(0, 1))
		obrazok("example.bmp");
	else
		printf("Nema riesenie\n");
	return 0;
}
