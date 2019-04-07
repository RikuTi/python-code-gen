import random
import string
import time

variable_types = ["std::string","int","float","bool"]
math_operations = ["+","-","/","^"]

def get_variable_int_value():
    return int(random.random() * 10000)

def get_variable_float_value():
    return float('{:.3f}'.format(random.random() * 10000)[:-1])

def get_variable_bool_value():
    choice = int(random.random())
    retn = "false"
    if(choice == 1):
        retn = "true"
    return retn


def get_variable_string_value(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return '\"' + ''.join(random.choice(chars) for _ in range(size)) + '\"'

global_variable_counter = 1
class_counter = 0


global_variables_pool = []
global_class_pool = []

class cpp_variable:
    def __init__(self,code,var_type,is_pointer=False,is_class=False):
        self.code = code
        self.var_type = var_type
        self.is_pointer = is_pointer
        self.is_class = is_class


class cpp_function:
    def __init__(self,ftype,name):
        self.type = ftype
        self.name = name

class cpp_class:
    def __init__(self,name,code,functions):
        self.name = name
        self.functions = functions
        self.references = 0
        self.code = code

    def addref(self):
        self.references += 1



def generate_global_random_variable():
    global variable_types
    global global_variable_counter

    retn = "invalid"
    index = int(random.random() * variable_types.__len__())

    if(index == 0): #std::string
        retn = "/*autogen*/" + variable_types[index] + " python_global_variable_" + str(global_variable_counter) + " = " + get_variable_string_value() + ";\n"
    elif(index == 1):#int
        retn = "/*autogen*/" + variable_types[index] + " python_global_variable_" + str(global_variable_counter) + " = " + str(get_variable_int_value())  + ";\n"
    elif(index == 2):#float
        retn = "/*autogen*/" + variable_types[index] + " python_global_variable_" + str(global_variable_counter) + " = " + str(get_variable_float_value())  + ";\n"
    elif(index == 3):#bool
        retn = "/*autogen*/" + variable_types[index] + " python_global_variable_" + str(global_variable_counter) + " = " + get_variable_bool_value()  + ";\n"

    create = cpp_variable(retn,variable_types[index])
    
    global_variable_counter += 1
    #add to our pool so we can reference them in code
    global_variables_pool.append(create)

    return retn

def get_random_value_from_type(var_type):
    retn = "0"
    if(var_type == "std::string"):
        retn =  get_variable_string_value()
    elif(var_type == "int"):
        retn = str(get_variable_int_value())
    elif(var_type == "float"):
        retn = str(get_variable_float_value())
    elif(var_type == "bool"):
        retn = str(get_variable_bool_value())

    return retn
    
def generate_local_random_variable(loc_index):
    
    global variable_types

    retn = "invalid"
    index = int(random.random() * variable_types.__len__())
    if(index == 0): #std::string
        retn = "/*autogen*/" + variable_types[index] + " python_local_variable_" + str(loc_index) + " = " + get_variable_string_value() + ";\n"
    elif(index == 1):#int
        retn = "/*autogen*/" + variable_types[index] + " python_local_variable_" + str(loc_index) + " = " + str(get_variable_int_value())  + ";\n"
    elif(index == 2):#float
        retn = "/*autogen*/" + variable_types[index] + " python_local_variable_" + str(loc_index) + " = " + str(get_variable_float_value())  + ";\n"
    elif(index == 3):#bool
        retn = "/*autogen*/" + variable_types[index] + " python_local_variable_" + str(loc_index) + " = " + get_variable_bool_value()  + ";\n"

    return retn, variable_types[index]

    
def generate_class_random_variable(loc_index):
    global variable_types
    retn = "invalid"
    index = int(random.random() * variable_types.__len__())
    if(index == 0): #std::string
        retn = variable_types[index] + " python_class_variable_" + str(loc_index) + ";\n"
    elif(index == 1):#int
        retn = variable_types[index] + " python_class_variable_" + str(loc_index) + ";\n"
    elif(index == 2):#float
        retn = variable_types[index] + " python_class_variable_" + str(loc_index) + ";\n"
    elif(index == 3):#bool
        retn = variable_types[index] + " python_class_variable_" + str(loc_index) + ";\n"

    return retn, variable_types[index]


def generate_random_class():
    global class_counter

    class_name = "python_class_" + str(class_counter)
    class_var_count = random.randint(4,10)
    class_variables = []
    class_functions = []
    for i in range(class_var_count):
        var_text, var_type = generate_class_random_variable(i)
        new_var = cpp_variable(var_text,var_type)
        class_variables.append(new_var)

    #private members
    vars_combined = ""
    for items in class_variables:
        vars_combined += "\t" + items.code

    #constructor values
    vars_construct_values = ""
    for items in class_variables:
        cur_text = items.code
        new_format = cur_text.replace(items.var_type,"")
        final_format = new_format.replace(";\n","")
        final_format = final_format.replace(" ","\t\t")
        final_format += " = " + get_random_value_from_type(items.var_type) + ";\n"
        vars_construct_values += final_format

    #functions to return private variables
    vars_created_functions = ""
    for items in class_variables:
        var_type = items.var_type
        cur_text = items.code
        new_format = cur_text.replace(items.var_type,"")
        final_format = new_format.replace(";\n","")
        final_format = final_format.replace(" ","")
        func_title = "\t" + var_type + "&" + " get_" + final_format + "()"
        func_body = "\t{\n\t\treturn " + final_format + ";\n\t}\n"
        vars_created_functions += func_title + "\n" + func_body + "\n"
        func = cpp_function(var_type," get_" + final_format)
        class_functions.append(func)

    format = "/*python_class_gen_begin*/\nclass " + class_name + "\n{\n" + "public:\n\t" + class_name + "()" + "\n"
    format += "\t{\n" + vars_construct_values + "\t}\n" + vars_created_functions +  "private:\n" + vars_combined + "};\n/*python_class_gen_end*/\n"

    class_counter += 1

    new_cpp_class = cpp_class(class_name,format,class_functions)

    global_class_pool.append(new_cpp_class)
    
    return format

def create_var_to_class():
    index = int(random.random() * global_class_pool.__len__())
    class_to_use = global_class_pool[index]

    is_pointer = bool(random.random() * 1)

    if(is_pointer == True):
        var_text = "/*autogen*/" + class_to_use.name + "* " + class_to_use.name + str(class_to_use.references) + " = " + "new " + class_to_use.name + "();\n"
    else:
        var_text =  "/*autogen*/" + class_to_use.name + " " + class_to_use.name + str(class_to_use.references) + ";\n"

    class_to_use.addref()

    var = cpp_variable(var_text,class_to_use.name,is_pointer,True)

    global_variables_pool.append(var)
        

file = open("codefile.cpp","r+")
random.seed(time.time())
#data = file.readlines()
temp_data = []

#clean up old generated code
should_erase = False

for line in file:

    if(line.find("/*python_class_gen_begin*/") != -1):
        should_erase = True
            
    if(line.find("/*autogen*/") == -1 and should_erase == False):
        temp_data.append(line)

    if(line.find("/*python_class_gen_end*/") != -1):
        should_erase = False

    


data = temp_data.copy()
for i in range(4):
    generate_random_class()

for i in range(10):
    generate_global_random_variable()



for class_data in global_class_pool:
    data.append(class_data.code)

for i in range(6):
    create_var_to_class()


for global_vars in global_variables_pool:
    data.append(global_vars.code)

class cpp_function_data:
    def __init__(self,bracket_right_positions,bracket_left_positions):
        self.right_pos = bracket_right_positions
        self.left_pos = bracket_left_positions


left_bracket_counter = 0
right_bracket_counter = 0

bracket_delta = 0
bracket_start = 0
bracket_end = 0
counter = 0
function_data = "none"
previous_line = ""
function_name = ""

parsed_functions = []
finished = False

left_brackets = []
right_brackets = []

for line in data:
    counter += 1

    if(line.find("class") == -1 and line.find("struct") == -1):
        for c in line:
            if(c == '{'):
                right_bracket_counter += 1
                if(bracket_start == 0):
                    function_name = previous_line + "{\n"
                    bracket_start = counter
                    right_brackets.append(counter)
                else:
                    right_brackets.append(counter+1)

            elif(c == '}'):
                left_bracket_counter += 1
                left_brackets.append(counter+1)
                if(left_bracket_counter == right_bracket_counter):
                    print("done")
                    bracket_end = counter

        previous_line = line

    if(left_bracket_counter > 0 and right_bracket_counter > 0 and left_bracket_counter == right_bracket_counter):
        #function_data = data[bracket_start:bracket_end]
        #function_data.insert(0,function_name)

        func_data = cpp_function_data(right_brackets,left_brackets)
        parsed_functions.append(func_data)

        left_brackets = []
        right_brackets = []
        right_bracket_counter = 0
        left_bracket_counter = 0
        bracket_start = 0
        bracket_end = 0

text,type_ = generate_local_random_variable(1)
if(parsed_functions.__len__() > 0):
    data.insert(parsed_functions[0].right_pos[0],text)

text2,type_2 = generate_local_random_variable(2)
data.insert(parsed_functions[0].right_pos[2],text2)

#function_as_string = ""
#for text in function_data:
#    function_as_string += text

#data.append(function_as_string)    

file.seek(0)
file.truncate(0)
for line in data:
    file.write(line)

file.close()
