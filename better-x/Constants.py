


WHITESPACE = set(["\n", " ", "\t"])

VALID_VAR_CHARS = set(["a", "b", "c", "d",
                       "e", "f", "g", "h",
                       "i", "j", "k", "l",
                       "m", "n", "o", "p", 
                       "q", "r", "s", "t", 
                       "u", "v", "l", "m", 
                       "n", "o", "p", "q",
                       "r", "s", "t", "u", 
                       "v", "w", "x", "y",
                       "z", "0", "1", "2",
                       "3", "4", "5", "6",
                       "7", "8", "9", "_"])


VALID_INT_SYMBOLS = set(["0", "1", "2", "3"
                         "4", "5", "6",
                         "7", "8", "9",
                         "+", "-", "*",
                         "/"])


VALID_FLOAT_SYMBOLS = set(["0", "1", "2", "3",
                         "4", "5", "6",
                         "7", "8", "9",
                         "+", "-", "*",
                         "/", "."])

NUMBERS = set(["0", "1", "2", "3",
                "4", "5", "6", "7",
                "8", "9"])

LOGICAL_OPERATORS = set(["+", "*", "-", "/",
                        "<", ">", "^", "&",
                        "%" ])

TYPE_CONVERSION =   {"i32": "int", 
                    "f32": "float",
                    "f64": "double",
                    "char[]": "char*",
                    "char": "char"}

NUMBER_TYPE = 1
STRING_TYPE = 2
CHAR_TYPE = 3
