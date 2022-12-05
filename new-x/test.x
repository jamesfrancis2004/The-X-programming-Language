


class Thing {
  i32 number = 100;
}

class OtherThing {
  i32 number = 1000;
  Thing thing = new Thing;
}

operation print_hello() {
  println "Hello, World!";
}


operation main() {
  i32 sum = 0; 
  loop i from 1 to 1000 {
    sum += i;
  }
  println "The sum is " sum;
  OtherThing thing = new OtherThing;
  sum += thing.thing.number;
  println "The sum is " sum;

  print_hello();

}
