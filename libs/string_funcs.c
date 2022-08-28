#include <stdlib.h>
#include <stdio.h>
#include <string.h>




//char* initialise_str(

void add_str(char* dest_str, char* source_str, int*dest_length, int source_length, int* max_length) {
        if (*dest_length + source_length + 1 >= *max_length) {
                while (*dest_length + source_length + 1 >= *max_length){
                        *max_length *= 2;
                }
                dest_str = (char*)realloc(dest_str, *max_length * sizeof(char));
                strncpy(&dest_str[*dest_length], source_str, source_length);
        } else {
                strncpy(&dest_str[*dest_length], source_str, source_length);
        }
        *dest_length = *dest_length + source_length;

        dest_length[*dest_length] = '\0';

}



