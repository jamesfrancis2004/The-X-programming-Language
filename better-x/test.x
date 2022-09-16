


operation sum(i32 num1, i32 num2) {
  i32 sum_var = num1 + num2;
  println "The sum of " num1 " and " num2 " is " sum_var;
}






operation main() {
  char[] name = "James";
  i32 age = 18;
  i32 other = 20;


  println "His name is " name " and he is " age " years old";
  
  loop i from 1 to 10 by 2 {
    println "The current iteration is " i;
  }
  sum(age, other);

}
