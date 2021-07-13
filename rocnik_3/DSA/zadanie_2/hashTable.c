#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashTable.h"

typedef struct node {
	char key[100];
	struct node* next;
} head;

void table_init(struct node*** table, int size) {
	*table = calloc(size, sizeof(struct node));

}

int hash(char str[]) {
	int len = strlen(str), h = 0;
	for (int i = 0; i < len; i++) {
		h = 31 * h + str[i];
	}
	return abs(h);
}



void insert(int prvocislo, char str[], struct node** table, int* poc) {

	int pos = hash(str) % prvocislo;

	struct node* akt = NULL;




	if (table[pos] == NULL) {
		akt = (struct node*)malloc(sizeof(struct node));
		*poc += 1;
		strcpy(akt->key, str);
		akt->next = NULL;
		table[pos] = akt;
	}
	else {
		akt = table[pos];
		while (akt != NULL) {
			if (strcmp(str, akt->key) == 0) {
				break;
			}
			else if (akt->next == NULL) {
				akt->next = (struct node*)malloc(sizeof(struct node));
				strcpy(akt->next->key, str);
				akt->next->next = NULL;
				akt = NULL;
			}
			else {
				akt = akt->next;
			}
		}
	}
}



int search(int prvocislo, char str[], struct node** table) {

	int pos = hash(str) % prvocislo;

	struct node* akt = NULL;

	if (table[pos] == NULL) {
		printf("nenachadza sa");
		return 0;
	}
	else {
		akt = table[pos];
		while (akt != NULL) {
			if (strcmp(str, akt->key) == 0) {
				//printf("nachadza sa");
				return 1;
			}
			else {
				akt = akt->next;
			}
		}
	}
	printf("nenachadza sa");
	return 0;
}

void table_resize(struct node*** table, int size, int old_size, int* poc) {
	*poc = 0;
	struct node** new_table;
	struct node* akt;
	table_init(&new_table, size);
	for (int i = 0; i < old_size; i++) {

		if ((*table)[i] != NULL) {
			akt = (*table)[i];
			while (akt != NULL) {
				insert(size, akt->key, new_table, poc);



				akt = akt->next;
			}
		}
	}

	free(*table);
	*table = new_table;
}