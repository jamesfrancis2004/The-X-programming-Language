#include <stdio.h>
#include <stdlib.h>
void sum(int num1,int num2){
 int sum_var = num1 + num2;
printf("The sum of %d and %d is %d\n",num1,num2,sum_var);
 }
void main(){
 char* name = "James";
int age = 18;
int other = 20;
printf("His name is %s and he is %d years old\n",name,age);
for (int i = 1; i < 10; i += 2) {
 printf("The current iteration is %d\n",i);
 }
sum(age, other);
 }
