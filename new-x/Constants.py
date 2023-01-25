from Class import Class
from i32 import i32
from Bool import Bool
from Operation import Operation
from Println import Println
from Loop import Loop
from Char_Array import CharArray
from If import If
from Elseif import Elseif
from Else import Else



TERMINATING_CHARACTERS = set([';', '}'])


SYMBOLS = set(["{", "}", ";", ",",
               "+", "-", "*", "/",
               ">", "=", "<", "."])


VALID_GLOBAL_KEYWORDS = {"op": Operation,
                         "class": Class}



PRIMITIVES = {"i32": i32,
              "bool": Bool,
              "f32": None,
              "f64": None,
              "char[]": CharArray}


BUILTINS = {"println": Println, 
            "loop": Loop,
            "if": If,
            "elseif": Elseif, 
            "else": Else}



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


LOGICAL_OPERATORS = set(["&&", "||"])



BOOLEAN_OPERATORS = set(["<", "<=", ">", ">=", "==", "!="])












