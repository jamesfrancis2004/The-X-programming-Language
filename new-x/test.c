#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
struct Square {
int width;
int height;
};
struct Square*  create_Square() {
 struct Square*  temp_value = malloc(sizeof(struct Square* ));
temp_value->width=100;
temp_value->height=50;
return temp_value;
}
struct Cube {
int depth;
struct Square*  square;
};
struct Cube*  create_Cube() {
 struct Cube*  temp_value = malloc(sizeof(struct Cube* ));
temp_value->depth=5;
temp_value->square=create_Square();
return temp_value;
}
void change_cube_depth(struct Cube*  cube){
cube->depth=100;
}
int main(){
struct Cube* cube=create_Cube();
change_cube_depth(cube);
int depth=cube->depth;
printf("the cube's new depth is %d\n", depth);
}

