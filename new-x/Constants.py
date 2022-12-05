import Parser
from i32 import i32
from Operation import Operation
from Println import Println
from Loop import Loop
from Char_Array import CharArray



TERMINATING_CHARACTERS = set([';', '}'])


SYMBOLS = set(["{", "}", ";", ",",
               "+", "-", "*", "/",
               ">", "=", "<", "."])


VALID_GLOBAL_KEYWORDS = {"operation": Operation,
                         "struct": None}



PRIMITIVES = {"i32": i32,
              "f32": None,
              "f64": None,
              "char[]": CharArray}


BUILTINS = {"println": Println, 
            "loop": Loop}



PRIMITIVE_EXPRESSION_BUILTINS = {"i32": None,
                                 "f32": None,
                                 "f64": None}

TYPE_CONVERSION = {None: "void", 
                   "i32": "int",
                   "f32": "float",
                   "f64": "double"}

VALID_ASSIGNMENT_OPERATORS = set(["=", "+=",
                                  "-=", "*=",
                                  "/="])
