void table_init(struct node*** table, int size);
int hash(char str[]);
void insert(int prvocislo, char str[], struct node** table, int* poc);
int search(int prvocislo, char str[], struct node** table);
void table_resize(struct node*** table, int size, int old_size, int* poc);