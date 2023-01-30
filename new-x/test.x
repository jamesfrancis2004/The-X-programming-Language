
class Square {
  i32 width = 5;
  i32 height = 10;
}


op build_square(i32 height, i32 width) -> Square {
  Square square = new Square;

  square.height = height;
  square.width = width;

  return square;

}

op power(i32 x, i32 n) -> i32 {
  if n == 0 {
    return 1;
  }

  if n & 1 == 1 {
    return x * power(x, n/2) * power(x, n/2);
  }

  return power(x, n/2) * power(x, n/2);

}



op main() -> i32 {
  i32 number = power(2, 28); # Power takes two numbers and returns the exponent
  println "2^28 is " number;
  Square square = build_square(10, 20);
  i32 width = square.width;
  i32 height = square.height;

  println "The square's width should be 20 and is " width;
  println "The square's height should be 10 and is " height;
  
}
