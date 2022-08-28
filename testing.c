#include <stdlib.h>


int main() {
        char* str = malloc(sizeof(char) * (5+1));
        memcpy(&str[0], "hello", 5);
        str[6] = '\0';
