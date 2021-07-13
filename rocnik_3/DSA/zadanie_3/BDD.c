#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>



struct BDD_node {
	struct BDD_node* one;
	struct BDD_node* zero;
	char* vector;
};

struct BDD {
	int var_sum;
	int node_sum;
	struct BDD_node* root;
};

struct BF {
	int var_sum;
	int node_sum;
	char* vector;
};



struct  BDD* create_BDD(struct BF* function) {
	char* vector = function->vector;
	struct BDD* diagram = (struct BDD*)malloc(sizeof(struct BDD));
	int vector_len = strlen(vector);
	struct BDD_node* root = (struct BDD_node*)malloc(sizeof(struct BDD_node));
	root->vector = (char*)malloc(strlen(vector) * sizeof(char));

	strcpy(root->vector, vector);
	function->node_sum++;
	int size = vector_len / 2;
	char* vec_l = (char*)malloc(size * sizeof(char));
	char* vec_r = (char*)malloc(size * sizeof(char));
	int j = 0;
	for (int i = 0; i < vector_len; i++) {

		if (i < vector_len / 2) {
			vec_l[i] = vector[i];
		}

		else {
			if (i == size) {
				vec_l[i] = '\0';
			}
			vec_r[j++] = vector[i];
		}
	}
	vec_r[j] = '\0';
	if (strlen(vec_l) == 1 && strlen(vec_r) == 1) {
		root->one = (struct BDD_node*)malloc(sizeof(struct BDD_node));
		root->one->vector = (char*)malloc(sizeof(char));
		root->zero = (struct BDD_node*)malloc(sizeof(struct BDD_node));
		root->zero->vector = (char*)malloc(sizeof(char));

		strcpy(root->zero->vector, vec_l);
		strcpy(root->one->vector, vec_r);
		root->zero->zero = NULL;
		root->zero->one = NULL;
		root->one->zero = NULL;
		root->one->one = NULL;
		function->node_sum += 2;
		diagram->root = root;
		return diagram;
	}
	else {
		function->vector = vec_l;
		struct BDD* zerooo = create_BDD(function);
		root->zero = zerooo->root;
		function->vector = vec_r;
		struct BDD* oneee = create_BDD(function);
		root->one = oneee->root;
	}
	diagram->var_sum = function->var_sum;
	diagram->node_sum = function->node_sum;
	diagram->root = root;
	return diagram;
}

/*int BDD_reduce(struct BDD *bdd){
	struct BDD *akt = bdd;
	struct BDD *aktt = bdd;
	struct BDD *zero = (struct BDD*)malloc(sizeof(struct BDD));
	struct BDD *one = (struct BDD*)malloc(sizeof(struct BDD));
	zero->one = NULL;
	zero->zero = NULL;
	zero->parent = NULL;
	zero->vector[0] = "0";
	zero->vector[0] = "\0";
	one->one = NULL;
	one->zero = NULL;
	one->parent = NULL;
	one->vector[0] = "1";
	one->vector[0] = "\0";

}*/


char BDD_use(struct BDD* bdd, char* vstupy) {
	int len = strlen(vstupy);
	struct BDD_node* akt = bdd->root;
	for (int i = 0; i < len; i++) {
		if (vstupy[i] == '1') {
			akt = akt->one;
		}
		else {
			akt = akt->zero;
		}
	}
	if (strlen(akt->vector) > 1) {
		return '-1';
	}
	return akt->vector[0];
}