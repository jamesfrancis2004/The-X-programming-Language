import re




valid_variable_name = re.compile(r"^((([a-zA-Z]|_)+[0-9]*)+)$")


new_char_array = re.compile(r"(char\[\d+\])")

number = re.compile(r"(.*)^\d(.*)")


generic_class_name = re.compile(r"^((([a-zA-Z]|_)+[0-9]*)+\[[a-zA-Z]+\])")


number_loop = re.compile(r".+ from .+ to .+( by .*)*")




if __name__ == "__main__":
    text = "i from 1 to 10"
    print(number_loop.match(text))
