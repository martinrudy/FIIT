#include <stdio.h>
#include <string.h>

void* pamat;








void addblock(void* p, void* konec, int len) {
	int newsize = ((len + 1) >> 1) << 1;												// zvýš o 1 a zarovnaj hore (na 2)
	int	oldsize = *(unsigned int*)p & ~0x1;												// zamaskuj najnižší bit

	if ((((oldsize - newsize) - sizeof(unsigned int*)) < 6) && newsize != oldsize) {
		newsize += (oldsize - newsize);
	}

	*(unsigned int*)p = newsize | 0x1;						// nastav novú dåžku

	if (newsize < oldsize) {
		*(unsigned int*)((char*)p + (newsize + sizeof(unsigned int*))) = newsize | 0x1;		// nastav dåžky v zostavájúcej
		if (((unsigned int*)((char*)p + (newsize + (2 * sizeof(unsigned int*))))) < konec){
			*(unsigned int*)((char*)p + (newsize + (2 * sizeof(unsigned int*)))) = oldsize - newsize - (2 * sizeof(unsigned int*));
			*(unsigned int*)((char*)p + ((newsize + sizeof(unsigned int*)) + (oldsize - newsize))) = oldsize - newsize - (2 * sizeof(unsigned int*));
		}
	}
	else {
		*(unsigned int*)((char*)p + (newsize + sizeof(unsigned int*))) = newsize | 0x1;
	}
}

void* memory_alloc(unsigned int size) {
	unsigned int* pom = pamat;
	pom += 1;
	unsigned int* pamat_konec = pamat;
	(char*)pamat_konec += (*(unsigned int*)pamat);


	while (pom <= pamat_konec && (*pom & 1) || *pom < size) {
		if (pom >= pamat_konec) {
			break;
		}
		(char*)pom += 2 * sizeof(unsigned int*) + (*pom & -2);
	}

	if (pom >= pamat_konec) {
		return NULL;
	}

	addblock(pom, pamat_konec, size);

	
	pom += 1;
	return pom;
}
 
int memory_free(void* valid_ptr) {
	void* pom = valid_ptr;
	void* ptr = valid_ptr;
	(char*)valid_ptr -= sizeof(unsigned int*);
	
	if (memory_check(ptr)) {
		*(unsigned int*)valid_ptr = *(unsigned int*)valid_ptr & -2;
		*(unsigned int*)((char*)valid_ptr + (*(unsigned int*)valid_ptr + sizeof(unsigned int*))) = *(unsigned int*)valid_ptr & -2;
	}
	else {
		return 1;
	}

	int akt = *(unsigned int*)valid_ptr;
	int next = *(unsigned int*)((char*)pom + (akt + sizeof(unsigned int*)));
	int prev = *(unsigned int*)((char*)pom - 2 * sizeof(unsigned int*));

	//uvolnujem prvy blok
	if (valid_ptr == ((char*)pamat + sizeof(unsigned int*)) && next & 1) {
		return 0;
	}
	//uvolnujem prvy a nasledujuci je prazdny
	else if (valid_ptr == ((char*)pamat + sizeof(unsigned int*)) && (next & 1) == 0) {
		*(unsigned int*)valid_ptr = akt + next + 2 * sizeof(unsigned int*);
		*(unsigned int*)((char*)pom + *(unsigned int*)valid_ptr) = akt + next + 2 * sizeof(unsigned int*);
		memset(ptr, 0, *(unsigned int*)valid_ptr);
		return 0;
	}
	//uvolnujem posledny blok
	else if (((char*)pom + akt == (char*)pamat + (*(unsigned int*)pamat & -2)) && (prev & 1) == 1) {
		return 0;
	}
	//obsadeny predchadzajuci a nasledujuci blok 
	else if (prev & 1 && next & 1) {
		return 0;
	}

	//uvolnujem posledny, predchadzajuci je volny
	else if ((prev & 1) == 0 && next == 0) {
		*(unsigned int*)((char*)pom - (3 * sizeof(unsigned int*) + prev)) = prev + akt + 2 * sizeof(unsigned int*);
		*(unsigned int*)((char*)pom + (sizeof(unsigned int*) + akt)) = prev + akt + next + 4 * sizeof(unsigned int*);
		memset((unsigned int*)((char*)pom - (2 * sizeof(unsigned int*) + prev)), 0, prev + akt + next + 4 * sizeof(unsigned int*));
		return 0;
	}

	//volny nasledujuci a predchadzajuci
	else if((prev & 1) == 0 && (next & 1) == 0){
		*(unsigned int*)((char*)pom - (3 * sizeof(unsigned int*) + prev)) = prev + akt + next + 4 * sizeof(unsigned int*);
		*(unsigned int*)((char*)pom + (2 * sizeof(unsigned int*) + next + akt)) = prev + akt + next + 4 * sizeof(unsigned int*);
		memset((unsigned int*)((char*)pom - (2 * sizeof(unsigned int*) + prev)), 0, prev + akt + next + 4 * sizeof(unsigned int*));

		return 0;
	}
	//predchadzajuci volny a nasledujuci obsadeny
	else if ((prev & 1) == 0 && (next & 1) == 1) {
		*(unsigned int*)((char*)pom - (3 * sizeof(unsigned int*) + prev)) = akt + prev + 2 * sizeof(unsigned int*);
		*(unsigned int*)((char*)pom + akt) = akt + prev + 2 * sizeof(unsigned int*);
		memset((unsigned int*)((char*)pom - (2 * sizeof(unsigned int*) + prev)), 0, akt + prev + 2 * sizeof(unsigned int*));
		
		return 0;
	}
	//nasledujuci volny predchadzajuci obsadeny
	else if ((prev & 1) == 1 && (next & 1) == 0) {
		*(unsigned int*)valid_ptr = akt + next + 2 * sizeof(unsigned int*);
		*(unsigned int*)((char*)pom + (akt + next + 2 * sizeof(unsigned int*))) = akt + next + 2 * sizeof(unsigned int*);
		memset(pom, 0, (akt + next + 2 * sizeof(unsigned int*)));

		return 0;
	}
	
	return 1;
}

int memory_check(void* ptr) {
	unsigned int* pom = pamat;
	pom += 1;
	char* pamat_konec = pamat;
	(char*)pamat_konec += (*(unsigned int*)pamat);

	
	/*if (*(unsigned int*)((char*)ptr - sizeof(unsigned int*)) & 1) {										//blok je neuvolneny
		return 1;
	}*/

	while (pom < pamat_konec) {	//prehladavam blok po bloku
		
		//printf("%d", *(unsigned int*)pom);
		
		//*(unsigned int*)((char*)pom + ((*(pom) & -2) + sizeof(unsigned int*))) = 9;

		if (pom < ptr && ((char*)pom + ((*(pom) & -2) + sizeof(unsigned int*))) > ptr) {			//nachadza sa pointer medzi hlavickou a patickou?
			if ((*pom & 1) == 0) {																	//je blok uvolneny?		
				return 0;
			}
			else {
				return 1;
			}
		}
		pom = ((char*)pom + ((*(pom) & -2) + 2 * sizeof(unsigned int*)));					//posun na dalsi blok

	}
	
	return 0;
}

void memory_init(void* ptr, unsigned int size) {
	if (size % 2 != 0) {
		size += 1;
	}
	pamat = ptr;
	//memset(pamat, 0, size);
	*(unsigned int*)pamat = (size - sizeof(unsigned int*));
	*(unsigned int*)((char*)pamat + sizeof(unsigned int*)) = size - 3 * sizeof(unsigned int*);
}

int random(unsigned int min, unsigned int max) {
	return rand() % (max + 1 - min) + min;
}



void test(char* region, char** pointer, int minmem, int maxmem, int min, int max, int cyklicky) {
	unsigned int allocated = 0, mallocated = 0, allocated_count = 0, mallocated_count = 0;
	unsigned int i = 0;
	int random_memory = 0, random = 0;

	memset(region, 0, 100000);
	random_memory = (rand() % (maxmem - minmem + 1)) + minmem;
	memory_init(region + 500, random_memory);

	if (cyklicky) {
		int random_values[5];
		memset(random_values, 0, 5);
		int x = 0, min_random = max;
		int is_in = 0;

		for (int k = 0; k < 5; k++) {
			int rnd = (rand() % (max - min + 1)) + min;
			is_in = 0;
			for (int l = 0; l < 4; l++) {
				if (random_values[l] == rnd) {
					is_in = 1;
				}
			}
			if (is_in) {
				k--;
			}
			else {
				random_values[k] = rnd;
				if (min_random > rand) {
					min_random = rnd;
				}
			}
		}
		while (allocated <= random_memory - min_random) {
			if (x > 4) {
				x = 0;
			}
			random = random_values[x++];
			if (allocated + random > random_memory)
				continue;
			allocated += random;
			allocated_count++;
			pointer[i] = (char*)memory_alloc(random);
			if (pointer[i]) {
				i++;
				mallocated_count++;
				mallocated += random;
			}
		}
		for (int j = 0; j < i; j++) {
			if (memory_check(pointer[j])) {
				memory_free(pointer[j]);
			}
			else {
				printf("Error: Zly memory check.\n");
			}
		}
		
		float result = ((float)mallocated_count / allocated_count) * 100;
		float result_bytes = ((float)mallocated / allocated) * 100;
		printf("Velkost pamate o %d bytov, velkost blokov cyklicky %d %d %d %d %d: alokovanych %.2f%% blokov (%.2f%% bytov).\n", random_memory, random_values[0], random_values[1], random_values[2], random_values[3], random_values[4], result, result_bytes);

	}

	else {

		while (allocated <= random_memory - min) {
			random = (rand() % (max - min + 1)) + min;
			if (allocated + random > random_memory)
				continue;
			allocated += random;
			allocated_count++;
			pointer[i] = (char*)memory_alloc(random);
			if (pointer[i]) {
				i++;
				mallocated_count++;
				mallocated += random;
			}
		}
		for (int j = 0; j < i; j++) {
			if (memory_check(pointer[j])) {
				memory_free(pointer[j]);
			}
			else {
				printf("Error: Zly memory check.\n");
			}
		}
		memset(region + 500, 0, random_memory);

		float result = ((float)mallocated_count / allocated_count) * 100;
		float result_bytes = ((float)mallocated / allocated) * 100;
		printf("Velkost pamate o %d bytov, velkost blokov %d: alokovanych %.2f%% blokov (%.2f%% bytov).\n", random_memory, random, result, result_bytes);
	}
	
}

int main() {
	char region[100000];
	char* pointer[13000];
	srand(time(NULL));
	printf("\n");
	printf("SCENAR 1\n");
	printf("*------------------------------------------------------------------------------------------------------*\n");
	test(region, pointer, 50, 50, 8, 8, 0);
	test(region, pointer, 100, 100, 8, 8, 0);
	test(region, pointer, 200, 200, 8, 8, 0);
	printf("\n");
	test(region, pointer, 50, 50, 15, 15, 0);
	test(region, pointer, 100, 100, 15, 15, 0);
	test(region, pointer, 200, 200, 15, 15, 0);
	printf("\n");
	test(region, pointer, 50, 50, 24, 24, 0);
	test(region, pointer, 100, 100, 24, 24, 0);
	test(region, pointer, 200, 200, 24, 24, 0);
	printf("\n");
	printf("SCENAR 2\n");
	printf("*------------------------------------------------------------------------------------------------------*\n");
	test(region, pointer, 50, 50, 8, 24, 1);
	test(region, pointer, 100, 100, 8, 24, 1);
	test(region, pointer, 200, 200, 8, 24, 1);
	printf("\n");
	printf("SCENAR 3\n");
	printf("*---------------------------------------------------------------------------------------------------------------------------------------------*\n");
	test(region, pointer, 10000, 10000, 500, 5000, 1);
	printf("\n");
	printf("SCENAR 4\n");
	printf("*---------------------------------------------------------------------------------------------------------------------------------------------*\n");
	test(region, pointer, 50000, 50000, 8, 50000, 1);
	return 0;
}