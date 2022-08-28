i32 age = 18;
i32 other = 5;
f32 pi = 3.1315;
pi = pi * pi;


str greeting = "hello";
str world = ", World";
str name = "james";
str phrase = greeting world " and another string and his name is " name;

println "The phrase is:";
println phrase;

loop i from 1 to 10 by 1 {
        pi = pi * 1.23;
        if (pi > 10) {
                println "The value for pi is now greater than 10";
        }

}


loop i through phrase {
        println "The value for i is " i;
}


println "The value for pi is " pi;




