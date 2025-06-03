import compulator.helpers.math_parser as math_parser
import compulator.helpers.helper_functions as helper_functions
import compulator.helpers.formulas_and_constants as formulas_and_constants
from compulator.helpers.compulator_exception import CompulatorException

def _find_corresponding_open_bracket(input: str, starting_index: int) -> int:
    for i in range(starting_index-1, -1, -1):
        curr_char = input[i]
        if curr_char == '[': return i
    return -1

def _get_formula_name_and_args(inside_brackets: str) -> dict:
    for i in range(len(inside_brackets)):
        char = inside_brackets[i]
        if char == '(':
            end_of_formula_name = helper_functions.prev_char_index(inside_brackets, i)
            start_of_arguments = i
            break
    formula_name = inside_brackets[ : end_of_formula_name+1]
    args = inside_brackets[start_of_arguments : ]
    return {"formula_name": formula_name, "args": args}

#put parameters and arguments in list
def _put_values_in_list(string: str) -> list:
    values_list = []
    curr_val = ""
    for i in range(1, len(string) - 1): #adjust range to not include parentheses
        char = string[i]
        if char == ' ' or char == '\t': continue
        elif char == ',':
            values_list.append(curr_val)
            curr_val = ""
            continue
        else: curr_val += char
    #add last value to values_list
    values_list.append(curr_val)
    return values_list

def _plug_in_arguments(formula: str, arg_dict: dict) -> str:
    i = 0
    while i < len(formula):
        char = formula[i]
        if char == ']':
            closing_bracket_index = i
            open_bracket_index = _find_corresponding_open_bracket(formula, i)
            if open_bracket_index < 0: raise CompulatorException("Missing opening bracket")

            inside_brackets = formula[open_bracket_index+1 : closing_bracket_index].strip()
            if inside_brackets in arg_dict:
                formula = formula[ : open_bracket_index] + '(' + arg_dict[inside_brackets] + ')' + formula[closing_bracket_index+1 : ]
                i = 0
                continue
        i += 1
    return formula

def _simplify_args(args_list: list) -> None:
    for i in range(len(args_list)):
        args_list[i] = math_parser.solve_problem(args_list[i])

def _match_params_with_args(parameters: str, arguments: str) -> dict:
    params_in_list = _put_values_in_list(parameters)
    args_in_list = _put_values_in_list(arguments)
    if len(params_in_list) != len(args_in_list): raise CompulatorException("Parameters and arguments do not match")
    _simplify_args(args_in_list)
    
    arg_dict = {}
    for i in range(len(params_in_list)):
        arg_dict[params_in_list[i]] = args_in_list[i]

    return arg_dict

def _get_formula_value(formula_call: str) -> str:
    formula_info = _get_formula_name_and_args(formula_call)
    formula_name = formula_info["formula_name"]
    arguments = formula_info["args"]

    if formula_name in formulas_and_constants.reserved_functions:
        args_in_list = _put_values_in_list(arguments)
        _simplify_args(args_in_list)
        reserved_func_value = formulas_and_constants.get_reserved_function_value(formula_name, args_in_list)
        return reserved_func_value

    formulas_dict = formulas_and_constants.get_formulas()
    formula_name_with_parens = formula_name + "()"
    if formula_name_with_parens not in formulas_dict: raise CompulatorException("Formula not found")

    formula = formulas_dict[formula_name_with_parens]["formula"]
    params = formulas_dict[formula_name_with_parens]["parameter_list"]

    arg_dict = _match_params_with_args(params, arguments)

    formula_with_args = _plug_in_arguments(formula, arg_dict)
    return formula_with_args

def evaluate_input(input: str) -> str:
    i = 0
    while i < len(input):
        char = input[i]
        if char == ']':
            closing_bracket_index = i
            open_bracket_index = _find_corresponding_open_bracket(input, i)
            if open_bracket_index < 0: raise CompulatorException("Missing opening bracket")

            inside_brackets = input[open_bracket_index+1 : closing_bracket_index].strip()
            if inside_brackets[-1] == ')':
                formula_value = _get_formula_value(inside_brackets)
                input = input[ : open_bracket_index] + '(' + formula_value + ')' + input[closing_bracket_index+1 : ]
            else:
                constants = formulas_and_constants.get_constants()
                if inside_brackets in formulas_and_constants.reserved_constants:
                    constant_value = str(formulas_and_constants.reserved_constants[inside_brackets])
                elif inside_brackets in constants:
                    constant_value = constants[inside_brackets]
                else: raise CompulatorException("Constant not found")
                input = input[ : open_bracket_index] + '(' + constant_value + ')' + input[closing_bracket_index+1 : ]

            i = 0
            continue
        i += 1

    return math_parser.solve_problem(input)