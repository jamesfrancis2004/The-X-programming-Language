#include "string_funcs.c"



int main() {
        int str_length = 5;
        int str_max_length = 10;
        char* str = malloc(sizeof(char) * 10);
        strncpy(str, "hello", str_length + 1);
        int str2_length = 5;
        int str2_max_length = 10;
        char* str2 = malloc(sizeof(char)*10);
        strncpy(str2, "hello", str2_length + 1);
        add_str(str, str2, &str_length, str2_length, &str_max_length);
        printf("The value for str is %s", str);
        printf("And max_length is %d\n", str_max_length);
}

