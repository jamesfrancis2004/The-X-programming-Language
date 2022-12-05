# The-X-programming-Language
A programming language compiled into C that is fast and performant but also easy to use. There have been a few iterations of compilers for x. The current compiler is implemented in the new-x directory.
When looking at the python files it is evident X does not use any external python libraries. This is so that the compiler can be implemented in raw python without the use of external libraries.
Currently x is not complete programming language; however, it supports a range of features which are demonstrated in the test.x file for each directory.


To compile some x code into c code, in the "nex-x" directiory run the following command "python3 compile.py 'name of x file' "
For x to compile successfully it requires a working c gcc compiler.
