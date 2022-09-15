#include "libs/libraries.h"
 int main() { int name_len = 0;
int name_max_length = 10;
char* name = malloc(sizeof(char) * name_max_length);
add_str(name, "James", &name_len, 5, &name_max_length);
printf("the name is %s\n",name);
int phrase_len = 0;
int phrase_max_length = 10;
char* phrase = malloc(sizeof(char) * phrase_max_length);
add_str(phrase, "the name is ", &phrase_len, 12, &phrase_max_length);
add_str(phrase, name, &phrase_len, name_len, &phrase_max_length);
float age =  100.0;
int number =  20;
age =  number + age;
printf("%f\n",age);
for (int i = 0; i < phrase_len; ++i) {
printf("the char is %c\n",phrase[i]);
}
for (int i = 1; i < 10; i += 1) {
printf("The current iteration is %d\n",i);
}
int count =  10;
int other =  5;
count =  count + other;
printf("the value for count is %d\n",count);
}