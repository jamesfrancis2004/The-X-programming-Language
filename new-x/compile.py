from Tokenizer import Tokenizer
import os
import Errors
import Parser
import time
import sys

def read_file(file_name):
    with open(file_name, "r") as fp:
        text = fp.read()

    return text
 


if __name__ == "__main__":
    start = time.time()
    text = read_file(sys.argv[1])
    tokenizer = Tokenizer()
    tokenizer.tokenize_text(text)
    line_text = text.splitlines()
    parser = Parser.Parser(tokenizer.tokenized_text, line_text)
    parser.parse()
    if (Errors.bad_compilation):
        exit(0)
    else:
        fp = open("test.c", "w+")
        print("#include <stdio.h>\n#include<stdlib.h>\n" + parser.return_converted_code(), file=fp)
        fp.close()
        os.system("gcc -o test test.c -O2")
    
    print(f"Time to compile was {time.time() - start}")



 
