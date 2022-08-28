#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 int main() { int age =  18;
int other =  5;
float pi =  3.1315;
pi =  pi * pi;
char* greeting = malloc(sizeof(char) * (+ 6 + 1));
strncpy(&greeting[0], "hello", 5);
int greeting_len = 0+ 5;
greeting[greeting_len] = '\0';
char* world = malloc(sizeof(char) * (+ 8 + 1));
strncpy(&world[0], ", World", 7);
int world_len = 0+ 7;
world[world_len] = '\0';
char* name = malloc(sizeof(char) * (+ 6 + 1));
strncpy(&name[0], "james", 5);
int name_len = 0+ 5;
name[name_len] = '\0';
char* phrase = malloc(sizeof(char) * (+ greeting_len+ world_len+ 37+ name_len + 1));
strncpy(&phrase[0], greeting, greeting_len);
strncpy(&phrase[0+ greeting_len], world, world_len);
strncpy(&phrase[0+ greeting_len+ world_len], " and another string and his name is ", 36);
strncpy(&phrase[0+ greeting_len+ world_len+ 36], name, name_len);
int phrase_len = 0+ greeting_len+ world_len+ 36+ name_len;
phrase[phrase_len] = '\0';
printf("The phrase is:\n");
printf("%s\n",phrase);
for (int i = 1; i < 10; i += 1) {
pi =  pi * 1.23;
if (pi > 10)  {
printf("The value for pi is now greater than 10\n");
}
}
for (int i = 0; i < phrase_len; ++i) {
printf("The value for i is %c\n",phrase[i]);
}
printf("The value for pi is %f\n",pi);
}