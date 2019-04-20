import random
import string
import time


file_name = "codefile.cpp"
variable_types = ["std::string","int","float","bool"]
math_operations = ["+","-","/","^"]
float_functions = ["std::pow","std::ffloor","std::ceilf"]
def get_variable_int_value():
    return random.randint(1,10000)

def get_variable_float_value():
    result = float('{:.3f}'.format(random.random() * 10000)[:-1])
    if(result < 1):
        result = 1
    return result

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
    def __init__(self,name,code,var_type,is_pointer=False,is_class=False):
        self.name = name
        self.code = code
        self.var_type = var_type
        self.is_pointer = is_pointer
        self.is_class = is_class

    def getCodeWithoutType(self):
        temp = self.code
        raw = temp.replace(self.var_type,"")
        raw = raw.replace(" ","",1)
        return raw



class cpp_function:
    def __init__(self,ftype,name):
        self.type = ftype
        self.name = name

    def getRawName(self):
        temp = self.name
        temp = temp.replace(" ","",1)

        return temp

class cpp_class:
    def __init__(self,name,code,functions):
        self.name = name
        self.functions = functions
        self.references = 0
        self.code = code

    def addref(self):
        self.references += 1


class cpp_function_data:
    def __init__(self,bracket_right_positions,bracket_left_positions,local_variables,var_count = 0):
        self.right_pos = bracket_right_positions
        self.left_pos = bracket_left_positions
        self.var_count = 0
        self.local_variables = local_variables



def generate_global_random_variable():
    global variable_types
    global global_variable_counter

    retn = "invalid"
    index = int(random.random() * variable_types.__len__())


    name = "python_global_variable_" + str(global_variable_counter)
    if(index == 0): #std::string
        retn = "/*autogen*/" + variable_types[index] + " " + name + " = " + get_variable_string_value() + ";\n"
    elif(index == 1):#int
        retn = "/*autogen*/" + variable_types[index] + " " + name + " = " + str(get_variable_int_value())  + ";\n"
    elif(index == 2):#float
        retn = "/*autogen*/" + variable_types[index] + " " + name + " = " + str(get_variable_float_value())  + ";\n"
    elif(index == 3):#bool
        retn = "/*autogen*/" + variable_types[index] + " " + name + " = " + get_variable_bool_value()  + ";\n"

    create = cpp_variable(name,retn,variable_types[index])
    
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

    name = "python_local_variable_" + str(loc_index)

    if(index == 0): #std::string
        retn = "/*autogen*/" + variable_types[index] + " " + name + " = " + get_variable_string_value() + ";\n"
    elif(index == 1):#int
        retn = "/*autogen*/" + variable_types[index] + " " + name  + " = " + str(get_variable_int_value())  + ";\n"
    elif(index == 2):#float
        retn = "/*autogen*/" + variable_types[index] + " " + name  + " = " + str(get_variable_float_value())  + ";\n"
    elif(index == 3):#bool
        retn = "/*autogen*/" + variable_types[index] + " " + name + " = " + get_variable_bool_value()  + ";\n"

    return name, retn, variable_types[index]

    
def generate_class_random_variable(loc_index):
    global variable_types
    retn = "invalid"
    index = int(random.random() * variable_types.__len__())

    name = "python_local_variable_" + str(loc_index)
    
    if(index == 0): #std::string
        retn = variable_types[index] + " " + name + ";\n"
    elif(index == 1):#int
        retn = variable_types[index] + " " + name + ";\n"
    elif(index == 2):#float
        retn = variable_types[index] + " " + name + ";\n"
    elif(index == 3):#bool
        retn = variable_types[index] + " " + name + ";\n"

    return name, retn, variable_types[index]


def generate_random_class():
    global class_counter

    class_name = "python_class_" + str(class_counter)
    class_var_count = random.randint(4,10)
    class_variables = []
    class_functions = []
    for i in range(class_var_count):
        var_name, var_text, var_type = generate_class_random_variable(i)
        new_var = cpp_variable(var_name,var_text,var_type)
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

    format = "\n/*python_class_gen_begin*/\nclass " + class_name + "\n{\n" + "public:\n\t" + class_name + "()" + "\n"
    format += "\t{\n" + vars_construct_values + "\t}\n" + vars_created_functions +  "private:\n" + vars_combined + "};\n/*python_class_gen_end*/\n"

    class_counter += 1

    new_cpp_class = cpp_class(class_name,format,class_functions)

    global_class_pool.append(new_cpp_class)
    
    return format

def create_var_to_class():
    index = int(random.random() * global_class_pool.__len__())
    class_to_use = global_class_pool[index]

    is_pointer = random.randint(0,1)

    if(is_pointer == True):
        var_text = "/*autogen*/" + class_to_use.name + "* " + class_to_use.name + str(class_to_use.references) + " = " + "new " + class_to_use.name + "();\n"
    else:
        var_text =  "/*autogen*/" + class_to_use.name + " " + class_to_use.name + str(class_to_use.references) + ";\n"

    class_to_use.addref()

    var = cpp_variable(class_to_use.name,var_text,class_to_use.name,is_pointer,True)

    global_variables_pool.append(var)

#hacky and ugly to use externs to declare across c++ files
def create_extern_global_declarations():
    externs = ""
    for vars in global_variables_pool:
        declared = "/*autogen*/" + "extern " + vars.var_type + " " + vars.name + ";\n"
        externs += declared

def generate_func_call(data_type):

    specific_type = 0
    #use random
  #  if(data_type == 0):
    #int
   # elif(data_type == 1):

    function_var_count = 0

    wrote_func = False
    for variable in global_variables_pool:
        if(variable.is_class == True):
            for classes in global_class_pool:
                if(classes.name == variable.var_type):

                    func_index = random.randint(0,classes.functions.__len__())
                    use_direct = False

                    #direct pass instead of store in variable to use
                    if(use_direct == True):
                        func_call = "/*autogen*/" + variable.name + "->" + classes.functions[func_index].getRawName() + "();\n"
                    else:
                        func_call = "/*autogen*/" + classes.functions[func_index].type + " python_return_val_" + str(function_var_count) + " = " + variable.name + "->" + classes.functions[func_index].getRawName() + "();\n"

                    if(variable.is_pointer == False):
                        func_call = "/*autogen*/" + variable.name + "." + classes.functions[func_index].getRawName() + "();\n"

                    data.insert(parsed_functions[0].right_pos[0],func_call)
                    wrote_func = True
                    break
        if(wrote_func == True):
            break


def generate_variable_in_function(func):
    name, text,var_type = generate_local_random_variable(func.var_count)

    create = cpp_variable(name,text,var_type)
    
    func.local_variables.append(create)

    func.var_count += 1

def get_random_global_variable_by_type(wanted_type):
    found_vars = []
    for vars in global_variables_pool:
        if(vars.var_type == wanted_type):
            found_vars.append(vars.name)

    result = "failed"
    if(found_vars.__len__() > 0):
        idx = random.randint(0,found_vars.__len__() - 1)
        result = found_vars[idx]

    return result

file = open(file_name,"r+")
random.seed(time.time())
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

    

#create dummy data
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
should_skip_parse = False
is_in_restricted_area = False
skip_this_iteration = False
#parse and collect all functions skipping classes and structs
for line in data:
    counter += 1
    skip_once = False
    if(line.find("class") != -1 or line.find("struct") != -1):
        should_skip_parse = True

    #line commented ignore
    if(line.find("//") != -1):
        continue

    if(line.find("/*") != -1 ):
        is_in_restricted_area = True

    skip_this_iteration = False

    #go throught line character by character
    for c in line:
        if(c == '{' and is_in_restricted_area == False):
            right_bracket_counter += 1
        #    print("right bracket ",previous_line,counter)
            if(bracket_start == 0):
                print(previous_line)
                function_name = previous_line + "{\n"
                bracket_start = counter
                right_brackets.append(counter)
            else:
                right_brackets.append(counter+1)

        elif(c == '}' and is_in_restricted_area == False):
            left_bracket_counter += 1
            left_brackets.append(counter+1)
          #  print("left bracket ",previous_line,counter)
            if(left_bracket_counter == right_bracket_counter):
                bracket_end = counter
                print("matched function",counter)
                #need to skip cuz data collected is from class or struct
                if(should_skip_parse == True):
                    left_brackets = []
                    right_brackets = []
                    right_bracket_counter = 0
                    left_bracket_counter = 0
                    bracket_start = 0
                    bracket_end = 0
                    should_skip_parse = False
                    skip_this_iteration = True


    if(line.find("*/") != -1):
        is_in_restricted_area = False

    previous_line = line
    #parsed brackets and found full function
    if(left_bracket_counter > 0 and right_bracket_counter > 0 and left_bracket_counter == right_bracket_counter and skip_this_iteration == False and is_in_restricted_area == False):
        local_funcs = []
        func_data = cpp_function_data(
            right_brackets, left_brackets, local_funcs)
        parsed_functions.append(func_data)

        left_brackets = []
        right_brackets = []
        right_bracket_counter = 0
        left_bracket_counter = 0
        bracket_start = 0
        bracket_end = 0


#generate random local variables for each found function
for idx in range(parsed_functions.__len__()):
    num_funcs = random.randint(3,8)
    for i in range(num_funcs):
        generate_variable_in_function(parsed_functions[idx])

#write created variables into the functions... declared at start cuz compiler wont change memory regardless of which spot theyre in
num_variables_wrote = 0
offset = 0
test_write = True
for idx in range(parsed_functions.__len__()):
    #offset because we write to previous functions and it will be on offset by that amount
    offset += num_variables_wrote
    offset2 = -1
    num_variables_wrote = 0
    test_write = True
    for e in parsed_functions[idx].local_variables:
        offset2 += 1
        data.insert(parsed_functions[idx].right_pos[0] + offset,e.code)
        num_variables_wrote = num_variables_wrote + 1

        
        if(parsed_functions[idx].right_pos.__len__() > 1 and e.var_type != "std::string"):
            some_global = get_random_global_variable_by_type(e.var_type)
            if(some_global != "failed"):
                text = "/*autogen*/" + e.var_type + " python_local_result_" + str(offset2) + " = " + e.name + " + " + some_global + ";\n"
                data.insert(parsed_functions[idx].right_pos[1] + offset + offset2,text)
                num_variables_wrote = num_variables_wrote + 1


file.seek(0)
file.truncate(0)
for line in data:
    file.write(line)

file.close()
