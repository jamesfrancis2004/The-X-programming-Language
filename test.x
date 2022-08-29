
str greeting = "hello";
str world = ", World";
str other = "Program start";
str phrase = greeting world other "!" "Hello, World!";

println "The phrase is " phrase;

loop i through phrase {
        println "current char is " i;
}

loop i from 1 to 10 by 1 {
        if (i > 5) {
                println "the current iteration is " i;
        }
}



f32 pi = 3.1415;
i32 age = 18;
pi = pi + age;
println "the value for pi is " pi " and the phrase of greeting is " greeting;


