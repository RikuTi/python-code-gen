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
    return ''.join(random.choice(chars) for _ in range(size))

global_variable_counter = 1
class_counter = 0


global_variables_pool = []

class c_variable:
    def __init__(self,text,var_type,is_pointer=False,is_reference=False):
        self.text = text
        self.var_type = var_type
        self.is_pointer = is_pointer
        self.is_reference = is_reference


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

    create = c_variable(retn,variable_types[index])
    
    global_variable_counter += 1
    #add to our pool so we can reference them in code
    global_variables_pool.append(create)

    return retn

def get_random_value_from_type(var_type):
    retn = "0"
    if(var_type == "std::string"):
        retn = "\"" + get_variable_string_value() + "\""
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
    for i in range(class_var_count):
        var_text, var_type = generate_class_random_variable(i)
        new_var = c_variable(var_text,var_type)
        class_variables.append(new_var)

    #private members
    vars_combined = ""
    for items in class_variables:
        vars_combined += "\t" + items.text

    #constructor values
    vars_construct_values = ""
    for items in class_variables:
        cur_text = items.text
        new_format = cur_text.replace(items.var_type,"")
        final_format = new_format.replace(";\n","")
        final_format = final_format.replace(" ","\t\t")
        final_format += " = " + get_random_value_from_type(items.var_type) + ";\n"
        vars_construct_values += final_format

    #functions to return private variables
    vars_created_functions = ""
    for items in class_variables:
        var_type = items.var_type
        cur_text = items.text
        new_format = cur_text.replace(items.var_type,"")
        final_format = new_format.replace(";\n","")
        final_format = final_format.replace(" ","")
        func_title = "\t" + var_type + "&" + " get_" + final_format + "()"
        func_body = "\t{\n\t\treturn " + final_format + ";\n\t}\n"
        vars_created_functions += func_title + "\n" + func_body + "\n"

    format = "/*python_class_gen_begin*/\nclass " + class_name + "\n{\n" + "public:\n\t" + class_name + "()" + "\n"
    format += "\t{\n" + vars_construct_values + "\t}\n" + vars_created_functions +  "private:\n" + vars_combined + "};\n/*python_class_gen_end*/\n"

    class_counter += 1
    
    return format


        
#your wanted path
file = open("fileloc/codegen.cpp","r+")
random.seed(time.time())
data = file.readlines()
class_data = generate_random_class()
data.insert(0,class_data)

other_data = generate_random_class()
data.append(other_data)

file.seek(0)
file.truncate(0)
for line in data:
    file.write(line)

file.close()
