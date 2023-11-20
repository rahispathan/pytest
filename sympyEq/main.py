from flask import Flask, request, jsonify
from latex2sympy2 import latex2sympy, latex2latex
from timeout_decorator import timeout
from sympy import solve, latex, N
import multiprocessing
import time
import ast
import re
import queue

app = Flask(__name__)


# for stop process after 3 seconds of timeout

def solve_equation_with_timeout(equation, symbols, timeout):
    def worker():
        try:
            solution = solve(equation, symbols, dict=True)
            result_queue.put(solution)
        except Exception as e:
            result_queue.put(None)

    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=worker)
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        return None
    return result_queue.get()

# def is_equation_valid(equation):
#     # Define a regular expression pattern to check if there is content after "="
#     pattern = re.compile(r'=\s*(.*)')
#     # print(pattern)
#     # Search for the pattern in the equation
#     match = pattern.search(equation)

#     if match:
#         content_after_equals = match.group(1)
#         if content_after_equals:
#             # "The equation is valid and has content after the '=' sign."
#             return equation
#         else:
#             return remove_equals_sign(equation)
#             # "The equation is valid but has nothing after the '=' sign."
#     else:
#         return equation


def floor_to_two_decimal_places(number):
    rounded_number = round(number, 2)  # Round to two decimal places
    formatted_number = "{:.2f}".format(rounded_number)  # Format as a string with two decimal places
    return formatted_number.rstrip('0').rstrip('.')

def is_arithmetic_equation(equation):
    valid_operators = ['+', '-', '*', '/', ':']
    # Use regular expression to split based on arithmetic operators
    
    components = re.split(r'([+\-*/:])', equation.replace(" ", ""))

    # print(components)

    if len(components) % 2 != 1:
        # print('1', False)
        return False  # Incorrect number of components

    for i, component in enumerate(components):
        if i % 2 == 0:  # Operand position
            if not component.replace('.', '', 1).isdigit():
                # print('2', False)

                return False  # Operand is not numeric
        else:  # Operator position
            if component not in valid_operators:
                # print('3', False)
        
                return False  # Invalid operator

    # print(True)

    return True


def add_parentheses(match):
        return f'{match.group(1)} = ({match.group(2)})'

def add_parentheses_to_equations(equations):
    # Define a regular expression pattern to find equations with '=' sign
    equation_list = equations.split(",")
    add_parentheses_to_equations = []
    for equation in equation_list:
        equation_pattern = re.compile(r'(\S+)\s*=\s*(.*?)(?:,|$)', re.M)
        add_parentheses_to_equations.append(equation_pattern.sub(add_parentheses, equation))
        
    list_of_equations_with_parentheses = ",".join(add_parentheses_to_equations)
    # print(list_of_equations_with_parentheses)
    
    return list_of_equations_with_parentheses

def remove_equal_and_whitespace_at_end(equation):
    # Define a regular expression pattern to check if '=' is at the very end of the equation
    pattern = re.compile(r'=\s*$')

    # Search for the pattern in the equation
    match = pattern.search(equation)

    if match is not None and match.end() == len(equation):
        # Remove the '=' sign and any trailing white spaces at the end
        modified_equation = equation[:-len(match.group())]
        return modified_equation
    else:
        return equation

def replace_equals_sign_2(match):
    if match.group(1) == '=':
        return '='

def convert_latex_system_to_comma_separated_list(latex_system):
    """This function converts a LaTeX system of equations to a comma-separated list of equations."""
    
    # Regular expression pattern to match a LaTeX system of equations.
    latex_system_pattern1 = r"\\begin{array} { l } (.*?)\\end{array}"

    latex_system_pattern2 = r"\\begin{array} { c } (.*?)\\end{array}"

    latex_system_pattern3 = r"\\begin{array} { r } (.*?)\\end{array}"

    
    # Match the regular expression pattern against the LaTeX system of equations.
    match1 = re.search(latex_system_pattern1, latex_system)

    match2 = re.search(latex_system_pattern2, latex_system)

    match3 = re.search(latex_system_pattern3, latex_system)

    
    # Check if the input matches the pattern
    if match1 is not None:
        equations = match1.group(1)
    elif match2 is not None:
        equations = match2.group(1)
    elif match3 is not None:
        equations = match3.group(1)
    else:
        # If it doesn't match, return the original input
        return latex_system
    
    # Split the equations into a list.
    equation_list = equations.split("\\\\")
    
    # Remove the equal signs from the equations.
    comma_separated_equations = []
    for equation in equation_list:
        if re.search(r'=', equation):
            comma_separated_equations.append(re.sub(r'(=)', replace_equals_sign_2, equation))
    
    # Join the modified equations back together using the comma as the delimiter.
    comma_separated_list_of_equations = ",".join(comma_separated_equations)
    
    return comma_separated_list_of_equations

def extract_variables_from_formula(formula):
    names = [i.id for i in ast.walk(ast.parse(formula)) if isinstance(i, ast.Name)]
    return list(set(names))

def replace_equals_sign(match):
    if match.group(1) == '=':
        return '-'


@app.route('/AI_Math', methods=['POST', 'GET'])
def AI_Math():

    if request.method == 'POST':
        try:
            latex_systems = request.form['equations']
            print('input', latex_systems)
            comma_separated_list_of_equations = []

            comma_separated_equation = convert_latex_system_to_comma_separated_list(latex_systems)
            comma_separated_list_of_equations.append(comma_separated_equation)
                
            modified_equations_else = []
            modified_equations_if = []
        
            for equations_set in comma_separated_list_of_equations:
                if re.search(r',', equations_set):
                    if re.search(r'=|=', equations_set):
                        equations_set1 = add_parentheses_to_equations(equations_set)
                        equations_set = re.sub(r'(=)|=', replace_equals_sign, equations_set1)
                    modified_equations_if.append(equations_set)
                else:
                    modified_equations_else.append(equations_set)

            # print(modified_equations_if, modified_equations_else)

            for modified_equation in modified_equations_if:
                
                sympy_expr = latex2sympy(modified_equation)
                
                variables = extract_variables_from_formula(str(sympy_expr))
                # return variables

                
                pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

                # Filter the variables to keep only single alphabets
                filtered_variables = [var for var in variables if re.match(pattern, var)]

                variables = tuple(filtered_variables)   

                # timout is for 3 second if process takes more than 3 seconds than it will stop

                solution = solve_equation_with_timeout(sympy_expr, variables, timeout=3)
                if solution is not None:
                    latex_solution = latex(solution)
                    print('solution->sympy', latex_solution)
                    # print('type', type(latex_solution))
                    # output_string = latex_solution.replace("\\", "")
                    # return //jsonify({'data': None, 'message': 'The equation took too long to solve', 'status': 400})
                    return {'data': latex_solution, 'message': 'Successfully solved', 'status': 200}
                else:
                    print('The equation took too long to solve.')
                    return jsonify({'data': None, 'message': 'The equation took too long to solve', 'status': 400})

            for original_equation in modified_equations_else:
                # print("single equations---------->", original_equation)
                try:
                    print(remove_equal_and_whitespace_at_end(original_equation))
                    if(is_arithmetic_equation(remove_equal_and_whitespace_at_end(original_equation)) == True):
                        sol2 = latex2sympy(remove_equal_and_whitespace_at_end(original_equation))
                        Nsol = N(sol2)
                        l2l = floor_to_two_decimal_places(Nsol)
                        print("N", l2l)
                        return {'data': str(l2l), 'message': 'Successfully solved', 'status': 200}
                    else:
                        solutions = latex2latex(remove_equal_and_whitespace_at_end(original_equation))
                        l2l = solutions
                        print("l2l", l2l)
                        return {'data': l2l, 'message': 'Successfully solved', 'status': 200}

                        

                except Exception as e:
                    # print('exp', e)
                    return jsonify({'data': None, 'message': 'Equation not solvable', 'status': 400})
        
        except ValueError as ve:
            msg = f'ValueError: {ve}', 'error'
            return jsonify({'data': None, 'message': msg, 'status': 400})
        except SyntaxError as se:
            msg = f'SyntaxError: {se}', 'error'
            return jsonify({'data': None, 'message': msg, 'status': 400})
        except:
            msg =f'An error occurred: Incorrrect Equations', 'error'
            return jsonify({'data': None, 'message': msg, 'status': 400})
    else:
        return jsonify({'data': None, 'message': 'Select valid method', 'status': 400})



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8098)