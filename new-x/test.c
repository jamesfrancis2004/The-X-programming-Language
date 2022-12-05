#include <stdio.h>
#include<stdlib.h>
struct Thing {
int number;
};
struct OtherThing {
int number;
struct Thing*  thing;
};
void print_hello(){
printf("Hello, World!\n");
}
void main(){
int sum=0;
for (int i = 1;i<1000;++i){
sum+=i;
}
printf("The sum is %d\n", sum);
struct OtherThing*  thing=malloc(sizeof(struct OtherThing));
thing->number=1000;
thing->thing=malloc(sizeof(struct Thing));
thing->thing->number=100;
sum+=thing->thing->number;
printf("The sum is %d\n", sum);
print_hello();
}

