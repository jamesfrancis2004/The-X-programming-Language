#include "libraries.h"



int main() {
        int str_length = 0;
        int str_max_length = 10;
        char* str = malloc(str_max_length * sizeof(char));
        add_str(str, "hello", &str_length, 5, &str_max_length);
        add_str(str, str, &str_length, 5, &str_max_length);
}

