import re
import numpy


def handle_command(input_string: str):
    if input_string == "/exit":
        print("Bye!")
        quit()

    elif input_string == "/help":
        print("Operations supported: addition + and subtraction -, multiplication *,"
              " division / and parentheses (...). "
              "Variables are also supported. Negative numbers are only supported by assigning to variables.")
    else:
        print("Unknown command")


def handle_assignment(input_string: str):
    if input_string.count("=") > 1:
        print("Invalid assignment")

    else:
        pattern = r"(\w+)\s*=\s*(\-?\w+)"
        match = re.match(pattern, input_string)
        new_variable = match.group(1)
        new_value = match.group(2)

        if not new_variable.isalpha():
            print("Invalid identifier")
        else:
            try:
                var_dict[new_variable] = int(new_value)
            except ValueError:
                if new_value.isalpha():  # check existing variables
                    if new_value in var_dict:  # match
                        var_dict[new_variable] = var_dict[new_value]
                    else:  # not match
                        print("Unknown variable")
                else:  # invalid variable name
                    print("Invalid assignment")


def value_present(input_string: str):
    if " " in input_string:
        print("Invalid expression")

    elif input_string.isdigit():  # nums
        print(int(input_string))

    elif not input_string.isalpha():  # alpha + num
        print("Invalid identifier")

    else:  # variable
        if input_string in var_dict:
            print(var_dict[input_string])
        else:
            print("Unknown variable")


def check_type(character: str) -> str:
    """Classify the type of characters"""
    if character.isalnum():
        return "ALNUM"
    if character in {"(", ")"}:
        return "SPECIAL_OPERATOR"
    return "BASIC_OPERATOR"


def split_string(input_string: str) -> list:
    # 1. remove all the spaces
    no_space_string = input_string.replace(" ", "")

    # 2. compare different type of single character
    # basic case
    new_string = no_space_string[0]
    comparison_type = check_type(new_string)

    for i in no_space_string[1:]:
        current_type = check_type(i)

        # if same type, only add a space when it's "(" or ")"
        if comparison_type == current_type:
            if current_type == "SPECIAL_OPERATOR":
                new_string += " "

        # if different type, add space and record the new type for comparison
        else:
            new_string += " "
            comparison_type = current_type

        new_string += i

    # 3. split the string to list
    list_for_cal = new_string.split()

    return list_for_cal


def variable_valid(lst: list) -> bool:
    """Return True if variable exists. If false, present reasons """
    for item in lst:
        if item.isalnum() and (not item.isdigit()):  # not operators and not nums
            if item.isalpha():
                if item in var_dict:
                    return True
                print("Unknown variable")
                return False
            else:  # invalid variable name (name with numbers)
                print("Invalid identifier")
                return False
    return True


def start_end_valid(lst: list):
    """Return True if start and end are alphas or numbers or '(', ')' """
    # check start
    if any(i in lst[0] for i in {"+", "-", "*", "/", ")"}):
        print("Invalid expression")
        return False

    # check end
    if any(i in lst[-1] for i in {"+", "-", "*", "/", "("}):
        print("Invalid expression")
        return False

    return True


def handle_operators(lst: list):
    for index, item in enumerate(lst):
        if isinstance(item, str):  # only check operators
            # check "+"
            if all(i == "+" for i in item):
                lst[index] = "+"

            # check "-", "--"
            elif all(i == "-" for i in item):
                if len(item) % 2 == 0:
                    lst[index] = "+"
                else:
                    lst[index] = "-"

            # check "-+", "+-"
            elif item in {"-+", "+-"}:
                lst[index] = "-"

            # check invalid expression
            else:
                if len(item) > 1:
                    print("Invalid expression")
                    return None

    # check "(" and ")"
    if lst.count("(") != lst.count(")"):
        print("Invalid expression")
        return None

    return lst


def calculate_ori(lst):
    if isinstance(lst[0], str):
        result = var_dict[lst[0]]
    else:
        result = lst[0]

    for i in range(len(lst) // 2):
        if isinstance(lst[2 * i + 2], str):
            current_value = var_dict[lst[2 * i + 2]]
        else:
            current_value = lst[2 * i + 2]

        if lst[2 * i + 1] == "+":
            result += current_value
        else:
            result -= current_value

    return result


def infix_to_postfix(infix: list) -> list:
    stack = []
    result = []
    for item in infix:

        # operands
        if item not in OPERATORS:
            # 1. Add operands (numbers and variables) to the result (postfix notation) as they arrive.
            result.append(item)

        # operators
        else:

            # 2. If the stack is empty or contains a left parenthesis on top,
            # push the incoming operator on the stack.
            if not stack or stack[-1] == "(":
                stack.append(item)

            # 5. If the incoming element is a left parenthesis, push it on the stack.
            elif item == "(":
                stack.append(item)

            # 6. If the incoming element is a right parenthesis,
            # pop the stack and add operators to the result until you see a left parenthesis.
            # Discard the pair of parentheses.
            elif item == ")":
                while stack[-1] != "(":
                    result.append(stack.pop())
                stack.pop()

            else:
                # 3. If the incoming operator has higher precedence than the top of the stack, push it on the stack.
                if item in OPERATORS_HIGH and stack[-1] in OPERATORS_LOW:
                    stack.append(item)

                # 4.If the precedence of the incoming operator is lower than or equal to that of the top of the stack,
                # pop the stack and add operators to the result until you see an operator that has smaller precedence or a left parenthesis on the top of the stack;
                # then add the incoming operator to the stack.
                else:
                    while stack and (stack[-1] not in OPERATORS_LOW or stack[-1] != "("):
                        result.append(stack.pop())
                    stack.append(item)

    # 7. At the end of the expression, pop the stack and add all operators to the result.
    while stack:
        result.append(stack.pop())

    return result


def calculate(postfix_list: list) -> int:
    stack = []
    for item in postfix_list:
        # If the incoming element is a number, push it into the stack
        if isinstance(item, int):
            stack.append(item)

        # If the incoming element is the name of a variable, push its value into the stack.
        elif item.isalpha():
            value = var_dict[item]
            stack.append(value)

        # If the incoming element is an operator,
        # then pop twice to get two numbers and perform the operation;
        # push the result on the stack.
        else:
            a = stack.pop()
            b = stack.pop()
            result = basic_calculation(b, a, item)  # pay attention: the inner - the outer
            stack.append(result)

    # When the expression ends, the number on the top of the stack is a final result.
    return stack[-1]


def basic_calculation(a: int, b: int, operator: str) -> int:
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        return int(numpy.round(a / b))


var_dict = {}
OPERATORS = {"+", "-", "*", "/", "(", ")"}
OPERATORS_HIGH = {"*", "/", "(", ")"}
OPERATORS_LOW = {"+", "-"}


def main():
    while True:
        string = input().strip()

        if not string:
            continue

        # handle command "/"
        if string.startswith("/"):
            handle_command(string)

        # Variable assignments
        elif "=" in string:
            handle_assignment(string)

        # no operators, show variable value
        elif all(i not in string for i in OPERATORS):
            value_present(string)

        # calculation
        else:
            expression_list = split_string(string)

            # if start with "+" or "-", add a "0" to the beginning (deal with "-3", "+5")
            if expression_list[0] in {"+", "-"}:
                expression_list = ["0"] + expression_list

            if variable_valid(expression_list) and start_end_valid(expression_list):
                # change number to int
                expression_list = [int(i) if i.isdigit() else i for i in expression_list]

                expression_list = handle_operators(expression_list)

                if expression_list:
                    postfix = infix_to_postfix(expression_list)
                    result = calculate(postfix)
                    print(result)


if __name__ == "__main__":
    main()