



class Square {
  i32 width = 100;
  i32 height = 50;

}


class Cube {
  i32 depth = 5;
  Square square = new Square;
}



op change_cube_depth(Cube cube) {
  cube.depth = 100;
}

op main() -> i32 {
  Cube cube = new Cube;
  change_cube_depth(cube);
  i32 depth = cube.depth;
  println "the cube's new depth is " depth;


}
