typedef struct Ht_item Ht_item;
// Define the Hash Table Item here
struct Ht_item {
    char* key;
    char* value;
};
typedef struct LinkedList LinkedList;
// Define the Linkedlist here
struct LinkedList {
    Ht_item* item;
    LinkedList* next;
};
typedef struct HashTable HashTable;

// Define the Hash Table here
struct HashTable {
    // Contains an array of pointers
    // to items
    Ht_item** items;
    LinkedList** overflow_buckets;
    int size;
    int count;
};
HashTable* create_table(int size);
void free_table(HashTable* table);
void ht_insert(HashTable* table, char* key, char* value);
char* ht_search(HashTable* table, char* key);
void print_search(HashTable* table, char* key);
