from latex2sympy2 import latex2sympy, latex2latex, set_real, handle_exp
import sympy
from timeout_decorator import timeout
from sympy import symbols, solve, simplify, preview, sympify, nsolve, latex, pprint, linsolve, nsimplify, Rel, N
import ast
import csv
import re

@timeout(3) 
def solve_with_timeout(equation, symbols, timeout=3):
  start_time = time.time()
  while time.time() - start_time < timeout:
    try:
      solution = solve(equation, symbols, dict=True)
      break
    except Exception as e:
      pass

    if time.time() - start_time > timeout:
        raise TimeoutError('The equation took too long to solve.')

  return solution

# def is_equation_valid(equation):
#     # Define a regular expression pattern to check if there is content after "="
#     pattern = re.compile(r'=\s*(.*)')

#     # Search for the pattern in the equation
#     match = pattern.search(equation)

#     if match:
#         content_after_equals = match.group(1)
#         if content_after_equals:
#             # "The equation is valid and has content after the '=' sign."
#             return equation
#         else:
#             return remove_equal_at_end(equation)
#             # "The equation is valid but has nothing after the '=' sign."
#     else:
#         return equation

def floor_to_two_decimal_places(number):
    rounded_number = round(number, 2)  # Round to two decimal places
    formatted_number = "{:.2f}".format(rounded_number)  # Format as a string with two decimal places
    return formatted_number.rstrip('0').rstrip('.')

def is_arithmetic_equation(equation):
    valid_operators = ['+', '-', '*', '/', ':', '%']
    # Use regular expression to split based on arithmetic operators
    
    components = re.split(r'([+\-*/:%])', equation.replace(" ", ""))

    print(components)

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

# Modify the function to add parentheses around the right-hand side
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
    
def replace_exponent(match):
    if match.group(1) == '^':
        return '^'

def convert_latex_system_to_comma_separated_list(latex_system):
    """This function converts a LaTeX system of equations to a comma-separated list of equations."""
    
    # Regular expression pattern to match a LaTeX system of equations.
    latex_system_pattern = r"\\begin{array} { l } (.*?)\\end{array}"
    
    # Match the regular expression pattern against the LaTeX system of equations.
    match = re.search(latex_system_pattern, latex_system)
    
    # Check if the input matches the pattern
    if match is not None:
        equations = match.group(1)
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

    
latex_systems = input()


def get_solve(latex_systems):
    
        comma_separated_list_of_equations = []

        comma_separated_equation = convert_latex_system_to_comma_separated_list(latex_systems)
        comma_separated_list_of_equations.append(comma_separated_equation)
            
        modified_equations_else = []
        modified_equations_if = []
        modified_equations_non_lin = []
        


        for equations_set in comma_separated_list_of_equations:
            if re.search(r',', equations_set):
                if re.search(r'=|=', equations_set):
                    equations_set1 = add_parentheses_to_equations(equations_set)
                    modified_equation = re.sub(r'(=)|=', replace_equals_sign, equations_set1)
                    if '^' in modified_equation:
                        modified_equations_non_lin.append(modified_equation)
                    else:
                        modified_equations_if.append(modified_equation)
                else:
                    modified_equations_else.append(equations_set)
            else:
                modified_equations_else.append(equations_set)
    
        # for modified_equation in modified_equations_non_lin:
        #     sympy_expr = latex2sympy(modified_equation)
        #     variables = extract_variables_from_formula(str(sympy_expr))
        #     # return variables            
        #     pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

        #     # Filter the variables to keep only single alphabets
        #     filtered_variables = [var for var in variables if re.match(pattern, var)]
        #     # print(filtered_variables)

        #     variables = tuple(filtered_variables)
        #     solutionSympy = linsolve(sympy_expr, variables)
        #     print('sys',solutionSympy)

        for modified_equation in modified_equations_non_lin:
            
            sympy_expr = latex2sympy(modified_equation)
            
            variables = extract_variables_from_formula(str(sympy_expr))
            # return variables

            
            pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

            # Filter the variables to keep only single alphabets
            filtered_variables = [var for var in variables if re.match(pattern, var)]
            # print(filtered_variables)

            variables = tuple(filtered_variables)
   

            try:
                solutions = solve_with_timeout(sympy_expr, list(variables))

                latex_solution = latex(solutionSympy)
                    
                print('solution->sympy', latex_solution)
            except TimeoutError:
                print('The equation took too long to solve.')
                result["Output"] = "Solving time exceeded"

                    
        # Print original equations (else)
        for original_equation in modified_equations_else:
            try:
                # print(remove_equal_at_end(original_equation))
                print('wiht=', remove_equal_and_whitespace_at_end(original_equation))
                if(is_arithmetic_equation(remove_equal_and_whitespace_at_end(original_equation)) == True):
                    sol2 = (remove_equal_and_whitespace_at_end(original_equation))
                    Nsol = floor_to_two_decimal_places(sol2)
                    print('Arithmetic->', N(Nsol))
                else:
                    solutions = latex2latex(remove_equal_and_whitespace_at_end(original_equation))
                    print('solution->latex2latex', solutions)
            except Exception as e:
                print('e', e)
                print('Equation not solvable')

get_solve(latex_systems)
