import compulator.helpers.helper_functions as helper_functions

operations = {
    '^': lambda x, y: x**y,
    '*': lambda x, y: x*y,
    '/': lambda x, y: x/y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y
}

def _is_negative_or_positive(expression: str, index: int) -> bool:
    #if there is no previous char, current num is negative/positive
    prev_char_index = helper_functions.prev_char_index(expression, index)
    if prev_char_index < 0: return True

    char_to_left = expression[prev_char_index]
    #1st condition, if character to the left of sign is '(', sign is used as negative num
    #2nd condition, if char to left is an operator, sign is used as negative num
    #3rd condition, if char to left is e (scientific notation, i.e. 10e-2), the sign is not part of the term
    if char_to_left == '(' or char_to_left in operations or char_to_left.lower() == 'e': return True

    #if char to left of sign is anything else, the minus sign is an operator for subtraction
    else: return False

def _get_corresponding_paren(expression: str, end_paren: int) -> int:
    #keeps track of unclosed end parens to the left of the end paren passed in to method
    end_paren_count = 1
    for i in range(end_paren - 1, -1, -1):
        if expression[i] == ')': end_paren_count += 1
        #open parens close the end paren, so end_paren_count is decremented 1 
        elif expression[i] == '(': end_paren_count -= 1

        #if end_paren_count gets to 0, the current character must be the corresponding open paren
        if end_paren_count == 0: return i
    return -1

def _get_sign_and_start_of_op(expression: str, starting_index: int, starting_paren: int, current_sign: str) -> dict:
    #if negative sign is found, sign will be replaced with '-'
    sign = current_sign
    #check chars to the left of innermost open paren to find negative signs
    for current_index in range(starting_index, -1, -1):
        char = expression[current_index]
        if (char == '-' or char == '+') and _is_negative_or_positive(expression, current_index):
            #following line says that if sign is '' (positive), sign becomes '-' (negative)
            #else it becomes positive
            sign = '-' if sign == '' and char == '-' else ''
        elif char == ' ': continue
        #if current char is to the left of the first opening paren of the term and
        #it's not a negative sign, the full term has been checked
        elif current_index < starting_paren: return {"sign": sign, "start_of_operation": current_index + 1}
    #if for loop exits, bounds has been reached
    return {"sign": sign, "start_of_operation": current_index}

def _in_front_of_e(expression: str, current_index: int) -> bool:
    #if there is no previous char, current num is not in front of e
    prev_char_index = helper_functions.prev_char_index(expression, current_index)
    if prev_char_index < 0: return False

    if expression[prev_char_index].lower() == 'e': return True

def _left_term_in_parens_info(expression: str, end_paren: int, start_paren: int) -> dict:
    current_index = start_of_term = end_paren
    sign = ''
    while True:
        current_index -= 1
        char = expression[current_index]
        #this term is in parens. Any sign found will not be operators because operations in parens
        #should already be solved (see solve_problem())
        if char == '-' or char == '+':
            if _in_front_of_e(expression, current_index): continue
            sign = '-' if char == '-' and sign == '' else ''
            continue
        elif char == ')': end_paren = current_index
        elif char == '(': break
        start_of_term = current_index
    sign_and_start_of_op = _get_sign_and_start_of_op(expression, current_index, start_paren, sign)
    sign = sign_and_start_of_op["sign"]
    start_of_op = sign_and_start_of_op["start_of_operation"]
    left_term = sign + expression[start_of_term : end_paren]
    return {"start_of_operation": start_of_op, "term": left_term}

def _left_term_no_parens_info(expression: str, operator_index: int, operation: str) -> dict:
    sign = ''
    #beginning_of_num is the index of the term's beginning without the sign
    current_index = beginning_of_term = operator_index
    #first_sign_found determines if the first sign (positive or negative) has been found
    #if first_sign_found is False, then no sign has been found
    first_sign_found = False
    while True:
        current_index -= 1
        #checking bounds
        if current_index < 0:
            beginning_of_term = 0 if first_sign_found == False else beginning_of_term
            break
        
        char = expression[current_index]
        if (char == '-' or char == '+') and _is_negative_or_positive(expression, current_index):
            if _in_front_of_e(expression, current_index): continue
            #if the first sign has NOT been found yet, set beginning of term to current_index + 1
            beginning_of_term = current_index + 1 if first_sign_found == False else beginning_of_term
            #first sign has been found, first_sign_found will always be True for the rest of the loop
            first_sign_found = True
            #if '-' is detected in term not in parens and the operator is '^',
            #break because the negative is not included in the term
            #ex. -9^2 == -81, '-' is not included in left term
            if operation == '^': break
            sign = '-' if char == '-' and sign == '' else ''
        
        #following conditions will check the beginning of the term
        #(this method is for terms not in parens)
        elif char in operations or char in '()':
            #if the first sign has NOT been found yet, set beginning of term to current_index + 1
            beginning_of_term = current_index + 1 if first_sign_found == False else beginning_of_term
            break
    left_term_info = {"start_of_operation": current_index + 1, "term": sign + expression[beginning_of_term : operator_index]}
    return left_term_info

def _get_left_term_info(expression: str, operator_index: int, operation: str) -> dict:
    #if there is an ending paren to the left of the operator,
    #begin_index is adjusted to get full term
    index_of_char_before_op = helper_functions.prev_char_index(expression, operator_index)
    if expression[index_of_char_before_op] == ')':
        #this condition should mean that the term is encapsulated in parens
        open_paren = _get_corresponding_paren(expression, index_of_char_before_op)
        term_info = _left_term_in_parens_info(expression, index_of_char_before_op, open_paren)
        begin_index = term_info["start_of_operation"] if operation != '^' else open_paren
        term = term_info["term"]
    else:
        term_info = _left_term_no_parens_info(expression, operator_index, operation)
        begin_index = term_info["start_of_operation"]
        term = term_info["term"]
    left_term_info = {"start_of_operation": begin_index, "term": term}
    return left_term_info

def _get_right_term_info(expression: str, operator_index: int) -> dict:
    #beginning index is inclusive in slicing, right of index is the beginning index
    current_index = end_of_term = operator_index
    start_of_term = helper_functions.next_char_index(expression, operator_index)
    sign = ''
    paren_count = 0

    while True:
        current_index += 1
        end_of_term = current_index
        #checking bounds
        length = len(expression)
        if current_index > length - 1:
            break

        char = expression[current_index]
        if char == '-' or char == "+":
            if _in_front_of_e(expression, current_index): continue
            elif _is_negative_or_positive(expression, current_index):
                sign = '-' if char == '-' and sign == '' else ''
                start_of_term = helper_functions.next_char_index(expression, current_index)
                continue
            else: break

        if char == '(':
            start_of_term = helper_functions.next_char_index(expression, current_index)
            paren_count += 1
        elif char == ')' or char in operations:
            break
        
    term = sign + expression[start_of_term : end_of_term]
    right_term_info = {"end_of_operation": end_of_term + paren_count, "term": term}
    return right_term_info

def _perform_operation(expression: str, operation: str, operator_index: int) -> str:
    left_term_info = _get_left_term_info(expression, operator_index, operation)
    right_term_info = _get_right_term_info(expression, operator_index)

    left_term = float(left_term_info["term"])
    right_term = float(right_term_info["term"])
    result = operations[operation](left_term, right_term)

    start_of_operation = left_term_info["start_of_operation"]
    end_of_operation = right_term_info["end_of_operation"]
    new_expression = expression[ : start_of_operation] + str(result) + expression[end_of_operation : ]
    return new_expression

#this method gets the correct char (see comments in method for details)
def _get_index(expression: str, char: str, char_count: int) -> int:
    #char_count helps get the right chararacter
    #e.g. the 2nd character will have a char_count of 2, so the method will return the index of the 2nd char found
    for i in range(len(expression)):
        if expression[i] == char: char_count -= 1
        #if char_count gets to 0, the current character must be the correct one
        if char_count == 0: return i
    return -1

def _count(expression: str, target: str) -> int:
    count = 0
    for char in expression:
        if char == target: count += 1
    return count

#checks operations in the current expression
def _solve_expression(expression: str) -> str:
    ordered_operations = (
        ('^'),
        ('*', '/'),
        ('+', '-')
    )
    for list_of_ops in ordered_operations:
        plus_sign_count = minus_sign_count = 0
        #checks if expression has operator
        has_operator = False
        for char in expression:
            if char in operations: has_operator = True
            if char in list_of_ops:
                sign = '+'
                if char == '-' or char == '+':
                    sign_count = 0
                    if char == '-':
                        minus_sign_count += 1
                        sign_count = minus_sign_count
                        sign = '-'
                    else:
                        plus_sign_count += 1
                        sign_count = plus_sign_count
                    operation_index = _get_index(expression, sign, sign_count)
                    if operation_index < 0 or _is_negative_or_positive(expression, operation_index): continue
                else: operation_index = _get_index(expression, char, 1)

                old_sign_count = _count(expression, sign)
                expression = _perform_operation(expression, char, operation_index)
                new_sign_count = _count(expression, sign)
                if sign == '+': plus_sign_count -= (old_sign_count - new_sign_count)
                else: minus_sign_count -= (old_sign_count - new_sign_count)
        #if has_operator is false, no need to check expression any further
        if has_operator == False: break
    return expression

def solve_problem(expression: str) -> str:
    #gets the number of end parens to determine how many inner expressions
    #should be solved first
    total_parens = _count(expression, ')')
    paren_count = 1
    for i in range(total_parens):
        #following line adjusts paren_count because it can change mid loop
        if i > 0:
            new_total_parens = _count(expression, ')')
            paren_count -= (total_parens - new_total_parens)
            total_parens = new_total_parens
        current_end_paren = _get_index(expression, ')', paren_count)
        current_open_paren = _get_corresponding_paren(expression, current_end_paren)
        
        expression_in_parens = expression[current_open_paren + 1 : current_end_paren]
        answer = str(_solve_expression(expression_in_parens))
        expression = expression[ : current_open_paren + 1] + answer + \
                    expression[current_end_paren : ]
        paren_count += 1
    answer = _solve_expression(expression)
    return helper_functions.simplify_answer(answer)