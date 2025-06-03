import json
import compulator.helpers.helper_functions as helper_functions
import math
import os
from compulator.helpers.compulator_exception import CompulatorException

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_FOLDER, "formulas_and_constants.json")

reserved_functions = {
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "tan": lambda x: math.tan(x),
    "arcsin": lambda x: math.asin(x),
    "arccos": lambda x: math.acos(x),
    "arctan": lambda x: math.atan(x),
    "sinh": lambda x: math.sinh(x),
    "cosh": lambda x: math.cosh(x),
    "tanh": lambda x: math.tanh(x),
    "arcsinh": lambda x: math.asinh(x),
    "arccosh": lambda x: math.acosh(x),
    "arctanh": lambda x: math.atanh(x),
    "log": lambda x, base=10: math.log(x, base),
    "ln": lambda x: math.log(x),
    "factorial": lambda x: math.factorial(int(x))
}

reserved_constants = {
    "pi": math.pi,
    "e": math.e
}

def get_reserved_function_value(formula_name: str, args: list) -> str:
    if len(args) == 1:
        return str(reserved_functions[formula_name](float(args[0])))
    elif len(args) == 2:
        return str(reserved_functions[formula_name](float(args[0]), float(args[1])))
    else:
        raise CompulatorException("Arguments don't match parameters in " + formula_name)

def reset_file() -> None:
    while True:
        confirm = input("Are you sure you want to clear all formulas and constants? (y or n)\n").strip().casefold()
        if confirm == 'y': break
        elif confirm == 'n': return
        else: print("Please enter y for yes or n for no")

    with open(JSON_PATH, "w") as f:
        file_data = {
            "formulas": {},
            "formulas_in_order": [],
            "constants": {},
            "constants_in_order": []
        }
        json.dump(file_data, f)

def _open_file(mode: str) -> None:
    try:
        f = open(JSON_PATH, mode)
    except:
        reset_file()
        f = open(JSON_PATH, mode)
    return f

def _update_and_close_file(f: json, file_data: dict) -> None:
    f.seek(0)
    json.dump(file_data, f)
    f.truncate()
    f.close()

def _overwrite_confirm(thing_to_overwrite: str) -> bool:
    while True:
        overwrite = input(f"'{thing_to_overwrite}' already exists. Do you want to overwrite it? (y or n)\n").strip().casefold()
        if overwrite == 'y': return True
        elif overwrite == 'n': return False
        else: print("Please enter y for yes or n for no")

def _store_formula(name: str, parameter_list: str, value: str) -> None:
    f = _open_file("r+")

    file_data = json.load(f)

    formulas = file_data["formulas"]
    formulas_in_order = file_data["formulas_in_order"]

    if (name + "()") in formulas:
        if _overwrite_confirm(name):
            formulas[name + "()"] = {"parameter_list": parameter_list, "formula": value}
    else:
        formulas[name + "()"] = {"parameter_list": parameter_list, "formula": value}
        helper_functions.insert_to_sorted(formulas_in_order, name)

    _update_and_close_file(f, file_data)

def _store_constant(name: str, value: str) -> None:
    f = _open_file("r+")

    file_data = json.load(f)

    constants = file_data["constants"]
    constants_in_order = file_data["constants_in_order"]

    if name in constants:
        if _overwrite_confirm(name):
            constants[name] = value
    else:
        constants[name] = value
        helper_functions.insert_to_sorted(constants_in_order, name)

    _update_and_close_file(f, file_data)

def create_formula_or_constant(formula_or_constant: str) -> None:
    formula_or_constant = formula_or_constant.strip()
    is_formula = False

    for i in range(len(formula_or_constant)):
        curr_char = formula_or_constant[i]
        if curr_char == '(':
            is_formula = True
            end_of_name = helper_functions.prev_char_index(formula_or_constant, i)
            start_of_parameters = i
        elif curr_char == '=':
            if is_formula:
                end_of_parameters = helper_functions.prev_char_index(formula_or_constant, i)
                if formula_or_constant[end_of_parameters] != ')':
                    raise CompulatorException("Invalid formula")
            else:
                end_of_name = helper_functions.prev_char_index(formula_or_constant, i)
            start_of_formula_or_const = helper_functions.next_char_index(formula_or_constant, i)
            break

    name = formula_or_constant[ : end_of_name + 1]
    value = formula_or_constant[start_of_formula_or_const : ]
    parameter_list = formula_or_constant[start_of_parameters : end_of_parameters + 1] if is_formula else None
    
    if (name in reserved_functions) or (name in reserved_constants):
        raise CompulatorException("Unable to create a reserved function/constant\n")

    if is_formula:
        _store_formula(name, parameter_list, value)
    else:
        _store_constant(name, value)

def _delete_confirm(thing_to_delete: str) -> bool:
    while True:
        user_confirm = input(f"Are you sure you want to delete '{thing_to_delete}'? (y or n)\n").strip().casefold()
        if user_confirm == 'y': return True
        elif user_confirm == 'n': return False
        else: print("Please enter y for yes or n for no")

def _remove_formula(formula_name: str) -> None:
    f = _open_file("r+")

    file_data = json.load(f)

    formulas = file_data["formulas"]
    formulas_in_order = file_data["formulas_in_order"]

    if formula_name not in formulas:
        raise CompulatorException("Formula not found")
    elif _delete_confirm(formula_name):
        formulas.pop(formula_name)
        helper_functions.remove_from_sorted(formulas_in_order, formula_name[ : len(formula_name)-2]) #get rid of parentheses
    
    _update_and_close_file(f, file_data)

def _remove_constant(constant_name: str) -> None:
    f = _open_file("r+")

    file_data = json.load(f)

    constants = file_data["constants"]
    constants_in_order = file_data["constants_in_order"]

    if constant_name not in constants:
        raise CompulatorException("Constant not found")
    elif _delete_confirm(constant_name):
        constants.pop(constant_name)
        helper_functions.remove_from_sorted(constants_in_order, constant_name)
    
    _update_and_close_file(f, file_data)

def remove_formula_or_constant(formula_or_constant_name: str) -> None:
    formula_or_constant_name = formula_or_constant_name.strip()
    if formula_or_constant_name[-1] == ')':
        _remove_formula(formula_or_constant_name)
    else:
        _remove_constant(formula_or_constant_name)

def get_formulas() -> dict:
    f = _open_file("r")
    file_data = json.load(f)
    formulas = file_data["formulas"]
    f.close()
    return formulas

def get_constants() -> dict:
    f = _open_file("r")
    file_data = json.load(f)
    constants = file_data["constants"]
    f.close()
    return constants

def print_formulas_and_constants() -> None:
    f = _open_file("r")
    file_data = json.load(f)

    formulas = file_data["formulas"]
    constants = file_data["constants"]
    formulas_in_order = file_data["formulas_in_order"]
    constants_in_order = file_data["constants_in_order"]

    print("Reserved Functions:")
    for curr_function in reserved_functions:
        print(curr_function)
    print()

    print("Reserved Constants:")
    for curr_constant in reserved_constants:
        print(curr_constant)
    print()

    print("Constants:")
    for curr_constant in constants_in_order:
        print(f"{curr_constant} = {constants[curr_constant]}")
    print()

    print("Formulas:")
    for curr_formula in formulas_in_order:
        formula_info = formulas[curr_formula + "()"]
        print(str(curr_formula) + str(formula_info["parameter_list"]) + " = " + str(formula_info["formula"]))
    print()