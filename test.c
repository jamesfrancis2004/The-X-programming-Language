#include "libs/libraries.h"
 int main() { int greeting_len = 0;
int greeting_max_length = 10;
char* greeting = malloc(sizeof(char) * greeting_max_length);
add_str(greeting, "hello", &greeting_len, 5, &greeting_max_length);
int world_len = 0;
int world_max_length = 10;
char* world = malloc(sizeof(char) * world_max_length);
add_str(world, ", World", &world_len, 7, &world_max_length);
int other_len = 0;
int other_max_length = 10;
char* other = malloc(sizeof(char) * other_max_length);
add_str(other, "Program start", &other_len, 13, &other_max_length);
int phrase_len = 0;
int phrase_max_length = 10;
char* phrase = malloc(sizeof(char) * phrase_max_length);
add_str(phrase, greeting, &phrase_len, greeting_len, &phrase_max_length);
add_str(phrase, world, &phrase_len, world_len, &phrase_max_length);
add_str(phrase, other, &phrase_len, other_len, &phrase_max_length);
add_str(phrase, "!", &phrase_len, 1, &phrase_max_length);
add_str(phrase, "Hello, World!", &phrase_len, 13, &phrase_max_length);
printf("The phrase is %s\n",phrase);
for (int i = 0; i < phrase_len; ++i) {
printf("current char is %c\n",phrase[i]);
}
for (int i = 1; i < 10; i += 1) {
if (i > 5)  {
printf("the current iteration is %d\n",i);
}
}
float pi =  3.1415;
int age =  18;
pi =  pi + age;
printf("the value for pi is %f and the phrase of greeting is %s\n",pi,greeting);
}