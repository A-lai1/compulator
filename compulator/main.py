import compulator.helpers.helper_functions as helper_functions
import compulator.helpers.formulas_and_constants as formulas_and_constants
import compulator.helpers.input_evaluation as input_evaluation
from compulator.helpers.compulator_exception import CompulatorException

def menu() -> None:
    print()
    print(":m for menu")
    print(":h for help")
    print(":a to add formulas and constants")
    print(":l to list stored formulas and constants")
    print(":r to remove stored formulas and constants")
    print(":c to clear all stored formulas and constants")
    print(":q to quit")
    print()

def help() -> None:
    print()
    print("The following are operators that the program accepts:")
    print("     '^': exponent")
    print("     '*': multiplication")
    print("     '/': division")
    print("     '+': addition")
    print("     '-': subtraction")
    print("Parentheses may be used")
    print("Roots should be typed in as exponents")
    print("     ex. square root would be 'x^(1/2)' or 'x^0.5'")
    print()

    print("To solve an expression, simply type in the expression")
    print()

    print("To create a formula, use the :a command")
    print("     :a nameOfFormula(a, b) = [a]^2 + [b]^2")
    print("Constants can also be created:")
    print("     :a pi = 3.14")
    print("To call a formula or constant, use the following format:")
    print("     [nameOfFormula(1, 2)]")
    print("     [pi]")
    print("Formulas and constants can be used within an expression:")
    print("     2 * [nameOfFormula(1, 2)]")
    print("     2 * [pi]")
    print("Formulas and constants can be used to make other formulas or constants:")
    print("     :a anotherFormula(a, b, c) = [c] + [nameOfFormula([a], [b])]")
    print("     (if parameters share the same name as constants, the arguments for the parameters will override the constant values)")
    print("     :a doublePi = 2 * [pi]")
    print("To delete a formula or constant, use the :r command followed by the name of the formula (followed by parentheses without parameters) or constant")
    print("     :r nameOfFormula()")
    print("     :r pi")
    print("To clear all formulas and constants, use the :c command")
    print("(FORMULAS AND CONSTANTS WILL NOT BE RECOVERABLE AFTER USING THIS COMMAND)")
    print()

    print("If error occurs:")
    print("- make sure expression is entered correctly")
    print("- make sure each opening parenthesis has a corresponding ending parenthesis and vice versa")
    print("     - ex. '(1+2' should be '(1+2)'")
    print("- make sure operators are correctly used")
    print("     - multiplication should always be defined with the '*' symbol")
    print("     - ex. '2(10 + 2)' should be written as '2*(10 + 2)'")
    print("- make sure you encapsulate formulas/constants/parameters in brackets")
    print("     - ex. 'a + b' should be '[a] + [b]'")
    print("- make sure numbers do not have commas in them")
    print("     - ex. '2,999' should be '2999'")
    print()

def list_formulas_and_constants() -> None:
    print()
    formulas_and_constants.print_formulas_and_constants()

def commands(user_input: str, colon_index: int) -> None:
    next_char_index = helper_functions.next_char_index(user_input, colon_index)
    next_char = user_input[next_char_index].casefold()
    match next_char:
        case 'm':
            menu()
        case 'h':
            help()
        case 'a':
            formulas_and_constants.create_formula_or_constant(user_input[next_char_index+1 : ])
            print()
        case 'l':
            list_formulas_and_constants()
        case 'r':
            formulas_and_constants.remove_formula_or_constant(user_input[next_char_index+1 : ])
            print()
        case 'c':
            formulas_and_constants.reset_file()
            print()
        case 'q':
            print("\nThank you for using Compulator")
            raise SystemExit
        case _:
            print("\nSorry, that is not a valid command")
            menu()

def run_compulator() -> None:
    print("Welcome to Compulator")
    menu()
    while True:
        try:
            print("Enter input below:")
            user_input = input()

            first_char_index = helper_functions.first_char_index(user_input)
            if first_char_index >= 0:
                first_char = user_input[first_char_index]
                if first_char == ':':
                    commands(user_input, first_char_index)
                else:
                    print(input_evaluation.evaluate_input(user_input))
                    print()
            else:
                print("\nPlease enter a valid input")
                menu()
        except SystemExit:
            raise SystemExit
        except CompulatorException as e:
            print(e)
            print()
        except:
            print("Sorry, something went wrong. Please try again. Use the :h command for help or the :m command for the menu\n")

if __name__ == "__main__":
    run_compulator()
