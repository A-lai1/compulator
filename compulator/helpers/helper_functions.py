#check if input begins with a backslash
def check_begins_backslash(input_string: str) -> int:
    for i in range(len(input_string)):
        if input_string[i] == '\\': return i
        #if char is not backslash or whitespace, input does not begin with backslash
        if input_string[i] != ' ' and input_string[i] != '\t': return -1
    return -1

#returns the index of the first char of a string that is not whitespace
def first_char_index(input_string: str) -> int:
    for i in range(len(input_string)):
        if input_string[i] != ' ' and input_string[i] != '\t': return i
    return -1

#this method gets the index of the next char, ignoring whitespace
def next_char_index(expression: str, current_index: int) -> int:
    for i in range(current_index + 1, len(expression)):
        if expression[i] != ' ' and expression[i] != '\t': return i
    return -1

#this method gets the index of the previous char, ignoring whitespace
def prev_char_index(expression: str, current_index: int) -> int:
    for i in range(current_index - 1, -1, -1):
        if expression[i] != ' ' and expression[i] != '\t': return i
    return -1

def get_corresponding_paren(expression: str, end_paren: int) -> int:
    #keeps track of unclosed end parens to the left of the end paren passed in to method
    end_paren_count = 1
    for i in range(end_paren - 1, -1, -1):
        if expression[i] == ')': end_paren_count += 1
        #open parens close the end paren, so end_paren_count is decremented 1 
        elif expression[i] == '(': end_paren_count -= 1

        #if end_paren_count gets to 0, the current character must be the corresponding open paren
        if end_paren_count == 0: return i
    return -1

#getIndex method gets the correct char (see comments in method for details)
def get_index(expression: str, char: str, char_count: int = 1) -> int:
    #char_count helps get the right chararacter
    #e.g. the 2nd character will have a char_count of 2, so the method will return the index of the 2nd char found
    for i in range(len(expression)):
        if expression[i] == char: char_count -= 1
        #if char_count gets to 0, the current character must be the correct one
        if char_count == 0: return i
    return -1

def remove_parens_and_spaces(result: str) -> str:
    new_result = ""
    for char in result:
        if char not in " ()":
            new_result += char
    return new_result

#removes extra signs if present in answer
def remove_extra_signs(result: str) -> str:
    sign = ''
    for i in range(len(result)):
        char = result[i]
        if char != '-' and char != '+': break
        sign = '-' if char == '-' and sign == '' else ''
    return sign + result[i : ]

#simplifies result if needed (multiple negatives, extra parens, etc.)
def simplify_answer(result: str) -> str:
    result = remove_parens_and_spaces(result)
    result = remove_extra_signs(result)
    return result

def insert_to_sorted(array: list, thing_to_insert: str) -> None:
    if len(array) == 0:
        array.append(thing_to_insert)
        return
    l = 0
    r = len(array) - 1
    while (l <= r):
        mid = (l + r) // 2
        if (mid == 0 and thing_to_insert < array[mid]) or ((array[mid-1] < thing_to_insert) and (array[mid] > thing_to_insert)):
            array.insert(mid, thing_to_insert)
            return
        elif array[mid] > thing_to_insert:
            r = mid - 1
        else:
            l = mid + 1
    #if loop exits (l > r), thing_to_insert does not go to the beginning or between values so it goes to the end
    array.append(thing_to_insert)

def remove_from_sorted(array: list, thing_to_remove: str) -> None:
    l = 0
    r = len(array) - 1
    while (l <= r):
        mid = (l + r) // 2
        if array[mid] < thing_to_remove:
            l = mid + 1
        elif array[mid] > thing_to_remove:
            r = mid - 1
        else:
            array.pop(mid)
            return