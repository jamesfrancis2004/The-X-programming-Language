#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
struct Square {
int width;
int height;
};
struct Square*  create_Square() {
 struct Square*  temp_value = malloc(sizeof(struct Square* ));
temp_value->width=5;
temp_value->height=10;
return temp_value;
}
struct Square*  build_square(int height, int width){
struct Square* square=create_Square();
square->height=height;
square->width=width;
return square;
}
int power(int x, int n){
if (n==0) {
return 1;
}
if (n&1==1) {
return x*power(x,n/2)*power(x,n/2);
}
return power(x,n/2)*power(x,n/2);
}
int main(){
int number=power(2,28);
printf("2^28 is %d\n", number);
struct Square* square=build_square(10,20);
int width=square->width;
int height=square->height;
printf("The square's width should be 20 and is %d\n", width);
printf("The square's height should be 10 and is %d\n", height);
}

