#include <stdio.h>
#include <stdlib.h>
void sum(int num1,int num2){
int sum_num = num1 + num2;
printf("The sum of %d + %d = %d\n",num1,num2,sum_num);
}

void main(){
int num1 = 1;
int num2 = 2;
char* name = "James";
sum(num1, num2);
printf("his name is %s\n",name);
}

