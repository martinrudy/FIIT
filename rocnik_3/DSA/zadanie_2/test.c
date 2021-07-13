#include "hashTable.h"
#include <stdio.h>
#include "bst.h"
#include <time.h>
#include <sys\timeb.h>
#include "hashTableDev.h"

#define CAPACITY1 1000003
#define CAPACITY2 2000003

int percento(int prv, int poc) {
	return (poc * 100) / prv;
}
//generovanie nahodnych cisel v rozmedzi
int randoms(int lower, int upper)
{
		int num = (rand() % (upper - lower + 1)) + lower;

		return num;
	
}
//test na vkladanie do prevzatej hash tabulky
void test_insert_into_htableDev(HashTable* ht, int scenar, int range) {
	if (scenar == 1) {
		for (int i = 0; i < range; i++) {
			char key[11];
			itoa(i, key, 10);
			ht_insert(ht, key, "Address");
		}
	}
	if (scenar == 2) {
		int last;
		int i;
		for (i = 0; i < range; i++) {
			char key[11];
			itoa(i, key, 10);
			ht_insert(ht, key, "Address");
			last = i;
		}
		char key[11];
		itoa(i, key, 10);
		ht_insert(ht, "1", "First address");
	}
	if (scenar == 3) {
		int extra_size = range + ((25 * range) / 100);
		for (int i = 0; i < range; i++) {
			char key[11];
			itoa(i, key, 10);
			ht_insert(ht, key, "Address");
		}
		for (int i = range; i <= extra_size; i++) {
			char key[11];
			itoa(i, key, 10);
			ht_insert(ht, key, "Address");
		}
	}
}
//test na vyhladavanie v prevzatej hash tabulke
void test_search_in_htableDev(HashTable* ht, int scenar, int range) {
	struct timeb start, end;
	int diff;
	if (scenar == 1) {
		for (int i = 0; i < range; i++) {
			char key[11];
			itoa(i, key, 10);
			ht_insert(ht, key, "Address");
		}
		ftime(&start);
		char search_key[11];
		int random_item = randoms(0, range);
		itoa(random_item, search_key, 10);
		print_search(ht, search_key);
		ftime(&end);
		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("\nOperation test_search_in_htableDev scenar 1 took %u milliseconds\n", diff);
	}
	if (scenar == 2) {
		for (int i = 0; i < range; i++) {
			char key[11];
			itoa(i, key, 10);
			ht_insert(ht, key, "Address");
		}
		ftime(&start);
		for (int i = 0; i < (5 * range) / 100; i++) {
			char search_key[11];
			int random_item = randoms(0, range);
			itoa(random_item, search_key, 10);
			print_search(ht, search_key);
		}
		ftime(&end);
		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("\nOperation test_search_in_htableDev scenar 2 took %u milliseconds\n", diff);
	}
}

//test na vkladanie do mojej hash tabulky
void test_insert_into_htableMy(struct node*** table, int scenar, int range, int *poc) {
	int prvocislo = CAPACITY1;
	int old_prvocislo;
	if (scenar == 1) {
		for (int i = 0; i < range; i++) {
			char buf[11];
			itoa(i, buf, 10);
			if (percento(prvocislo, *poc) >= 70) {
				old_prvocislo = prvocislo;
				prvocislo = CAPACITY2;
				table_resize(table, prvocislo, old_prvocislo, poc);
				//printf("%d", percento(prvocislo, *poc));
			}
			else {
				insert(prvocislo, buf, *table, poc);
			}
		}
	}
	if (scenar == 2) {
		int i;
		for (i = 0; i < range; i++) {
			char buf[11];
			itoa(i, buf, 10);
			if (percento(prvocislo, *poc) >= 70) {
				old_prvocislo = prvocislo;
				prvocislo = CAPACITY2;
				table_resize(table, prvocislo, old_prvocislo, poc);
				//printf("%d", percento(prvocislo, *poc));
			}
			else {
				insert(prvocislo, buf, *table, poc);
			}
		}
		char buf[11];
		itoa(i, buf, 10);
		insert(prvocislo, buf, *table, poc);
	}
	if (scenar == 3) {
		int extra_size = range + ((25 * range) / 100);
		for (int i = 0; i < range; i++) {
			char buf[11];
			itoa(i, buf, 10);
			if (percento(prvocislo, *poc) >= 70) {
				old_prvocislo = prvocislo;
				prvocislo = CAPACITY2;
				table_resize(table, prvocislo, old_prvocislo, poc);
				//printf("%d", percento(prvocislo, *poc));
			}
			else {
				insert(prvocislo, buf, *table, poc);
			}
		}
		for (int i = range; i < extra_size; i++) {
			char buf[11];
			itoa(i, buf, 10);
			if (percento(prvocislo, *poc) >= 70) {
				old_prvocislo = prvocislo;
				prvocislo = CAPACITY2;
				table_resize(table, prvocislo, old_prvocislo, poc);
				//printf("%d", percento(prvocislo, *poc));
			}
			else {
				insert(prvocislo, buf, *table, poc);
			}
		}
	}

}

//test na vyhladavanie v mojej hash tabulke
void test_search_in_htableMy(struct node* table, int scenar, int range, int* poc) {
	int prvocislo = CAPACITY1;
	int old_prvocislo;
	struct timeb start, end;
	int diff;
	for (int i = 0; i < range; i++) {
		char buf[11];
		itoa(i, buf, 10);
		if (percento(prvocislo, *poc) >= 60) {
			old_prvocislo = prvocislo;
			prvocislo = CAPACITY2;
			table_resize(table, prvocislo, old_prvocislo, poc);
			printf("%d", percento(prvocislo, *poc));
		}
		else {
			insert(prvocislo, buf, table, poc);
		}
	}
	if (scenar == 1) {
		ftime(&start);

		char search_key[11];
		int random_item = randoms(0, range);
		itoa(random_item, search_key, 10);
		search(prvocislo, search_key, table);

		ftime(&end);
		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("\nOperation test_search_in_htableMy scenar 1 took %u milliseconds\n", diff);
	}
	if (scenar == 2) {
		ftime(&start);
		for (int i = 0; i < (5 * range) / 100; i++) {
			char search_key[11];
			int random_item = randoms(0, range);
			itoa(random_item, search_key, 10);
			search(prvocislo, search_key, table);
		}
		ftime(&end);
		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("\nOperation test_search_in_htableMy scenar 2 took %u milliseconds\n", diff);
	}

}

//test na vyhladavanie v BVS
void test_search_bst(struct node* root, int scenar, int random, int range) {
	struct timeb start, end;
	int diff;
	srand(time(NULL));
	if (random) {

		for (int i = 0; i < range; i++) {
			root = insertnode(root, rand());
		}
	}
	else {
		for (int i = 0; i < range; i++) {
			root = insertnode(root, i);
		}
	}
	if (scenar == 1) {
		ftime(&start);

		int random_item = randoms(0, range);
		search_bst(root, random_item);

		ftime(&end);
		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("\nOperation test_search_bst scenar 1 took %u milliseconds\n", diff);
	}
	if (scenar == 2) {
		ftime(&start);
		for (int i = 0; i < (5 * range) / 100; i++) {
			int random_item = randoms(0, range);
			search_bst(root, random_item);
		}
		ftime(&end);
		diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
		printf("\nOperation test_search_bst scenar 2 took %u milliseconds\n", diff);
	}
	
}

//test na insertovanie do BST nahodnych cisel
void test_insert_bst_random(struct node ***root, int scenar, int range) {
	srand(time(NULL)); 
	if (scenar == 1) {
		for (int i = 0; i < range; i++) {
			*root = insertnode(*root, rand());
		}
	}
	if (scenar == 2) {
		for (int i = 0; i < range; i++) {
			*root = insertnode(*root, rand());
		}
		*root = insertnode(*root, rand());
	}
	if (scenar == 3) {
		int extra_size = range + ((25 * range) / 100);
		for (int i = 0; i < range; i++) {
			*root = insertnode(*root, rand());
		}
		for (int i = range; i <= extra_size; i++) {
			*root = insertnode(*root, rand());
		}
	}
	
}

//test na insertovanie do BST za sebou iduce cisla 
void test_insert_bst_inorder(struct node ***root, int scenar, int range) {
	if (scenar == 1) {
		for (int i = 0; i < range; i++) {
			*root = insertnode(*root, i);
		}
	}
	if (scenar == 2) {
		int i;
		for (i = 0; i < range; i++) {
			*root = insertnode(*root, i);
		}
		*root = insertnode(*root, i);
	}
	if (scenar == 3) {
		int extra_size = range + ((25 * range) / 100);
		for (int i = 0; i < range; i++) {
			*root = insertnode(*root, i);
		}
		for (int i = range; i <= extra_size; i++) {
			*root = insertnode(*root, i);
		}
	}
}

int main(void)
{
	char buf[10] = { 'i', 'd', 'n', 'm', 'j', 'H', 'K', 'a', 'a', '\0' };
	int prvocislo, poc = 0, prvocisla[3] = {1000003,  2000003, 4000037};
	int old_size, i = 0, diff;
	clock_t t;
	struct timeb start, end;

	struct node** table;
	struct Node* root = NULL;


	prvocislo = CAPACITY1;
	
	HashTable* ht = create_table(prvocislo);
	
	table_init(&table, prvocislo);


	/*ftime(&start);
	test_insert_into_htableMy(&table, 3, 100000, &poc);
	ftime(&end);
	diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
	printf("Operation test_insert_into_htableMy scenar 1 took %u milliseconds\n", diff);

	/*ftime(&start);
	test_insert_into_htableDev(ht, 1, 25000);
	ftime(&end);
	diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
	printf("Operation test_insert_into_htableDev scenar 1 took %u milliseconds\n", diff);


	/*ftime(&start);
	test_insert_bst_inorder(&root, 3, 100000);
	ftime(&end);
	diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
	printf("Operation test_insert_bst_inorder scenar 1 took %u milliseconds\n", diff);

	ftime(&start);
	test_insert_bst_random(&root, 3, 100000);
	ftime(&end);
	diff = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
	printf("Operation test_insert_bst_random scenar 1 took %u milliseconds\n", diff);*/

	test_search_in_htableMy(table, 1, 100000, &poc);
	test_search_in_htableDev(ht, 1, 100000);
	test_search_bst(root, 1, 0, 100000);
	

	return 0;
}