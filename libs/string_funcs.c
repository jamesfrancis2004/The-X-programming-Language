#include "string_funcs.h"

void add_char_str(char* dest_str, char source_char, int* dest_length, int* max_length) {
        if (*dest_length + 2 >= *max_length) {
                *max_length *= 2;
                dest_str = (char*) realloc(dest_str, *max_length * sizeof(char));
        }
        dest_str[*dest_length] = source_char;
        *dest_length += 1;
        dest_str[*dest_length] = '\0';
}



void add_str(char* dest_str, char* source_str, int* dest_length, int source_length, int* max_length) {
        if (*dest_length + source_length + 1 >= *max_length) {
                while (*dest_length + source_length + 1 >= *max_length){
                        *max_length *= 2;
                }
                dest_str = (char*)realloc(dest_str, *max_length * sizeof(char));
                strncpy(&dest_str[*dest_length], source_str, source_length);
        } else {
                strncpy(&dest_str[*dest_length], source_str, source_length);
        }
        *dest_length += source_length;
        dest_str[*dest_length] = '\0';
}

//void add_int_str(char* dest_str, int source_int, int* dest_length, int* max_length) {
        //char buffer[12];
        //itoa(source_int, buffer, 10);
        //add_str(dest_str, buffer, dest_length, strlen(buffer), max_length);
//}
         



