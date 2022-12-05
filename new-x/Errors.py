import sys
import Regex

bad_compilation = False

def println(str_mess):
    global bad_compilation
    bad_compilation = True
    print(str_mess, file=sys.stderr)

def normal_print(str_mess):
    global bad_compilation
    bad_compilation = True
    print(str_mess, file=sys.stderr, end="")

def printerror(str_mess):
    global bad_compilation
    bad_compilation = True
    print("\033[1m\033[91m" + str_mess + "\033[0m\033[0m", end="", file=sys.stderr)

def printbold(str_mess):
    global bad_compilation 
    bad_compilation = True
    print("\033[1m" + str_mess + "\033[0m", file=sys.stderr, end="")

def printboldln(str_mess):
    global bad_compilation
    bad_compilation = True
    print("\033[1m" + str_mess + "\033[0m", file=sys.stderr)

def line_error(str_mess, line_number):
    global bad_compilation 
    bad_compilation = True
    printerror(f"Error on line {line_number+1}: ")
    println(str_mess)

def isValidName(name, split_lines, line_count):
    if Regex.valid_variable_name.match(name) == None:
        global bad_compilation
        bad_compilation = True
        line_error(split_lines[line_count], line_count+1)
        normal_print("Bad variable name for ")
        printbold(name) 
        println(" ,consider redefining to valid variable name")
        return False

    return True


    

