#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "BDD.h"
#include <time.h>
#include <sys\timeb.h>


int randoms(int lower, int upper)
{
	
	int num = (rand() % (upper - lower + 1)) + lower;

	return num;

}

char* generate_vector(n) {
	srand(time(0));
	int vector_size = pow(2, n);
	char *vector = (char*)malloc(vector_size * sizeof(char));
	int i;
	for (i = 0; i < vector_size; i++) {
		int bit = randoms(0, 1);
		if (bit == 0) {
			vector[i] =  '0';
			//printf("bola to nulka\n");
		}
		else {
			vector[i] = '1';
			//printf("bola to jednotko\n");
		}
	}
	vector[i] = '\0';
	return vector;
}

int main()
{
	clock_t t;
	struct timeb start, end;
	int diff;

	for (int i = 12; i <= 20; i++) {
		ftime(&start);
		char* vector = generate_vector(i);
		struct BF* function = (struct BF*)malloc(sizeof(struct BF));
		function->var_sum = i;
		function->node_sum = 0;
		function->vector = vector;
		struct BDD* root = create_BDD(function);
		ftime(&end);

		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("v case: %dms, s poctom premennych: %d bolo vytvorenych %d uzlov\n", diff, root->var_sum, root->node_sum);
	}

	
	return 0;
}