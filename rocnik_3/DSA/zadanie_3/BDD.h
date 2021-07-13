
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
struct  BDD* create_BDD(struct BF* function);
char BDD_use(struct BDD* bdd, char* vstupy);
