from latex2sympy2 import latex2sympy, latex2latex
import sympy
from timeout_decorator import timeout
from sympy import symbols, solve, simplify, preview, sympify, nsolve, latex, pprint
from sympy.printing.mathml import print_mathml
import ast
import csv
import re
import time

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

def replace_equals_sign_2(match):
    if match.group(1) == '=':
        return '='

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



latex_systems = input()

# print('*->>')
# Example usage:
# latex_systems = [
#     r"\begin{array} { l } x ^ { 2 } + y ^ { 2 } = 4 \\ x ^ { 2 } - y ^ { 2 } = 4 \end{array}",
#     r"\begin{array} { l } x ^ { 2 } - y = 0 \\ y = x - 2 \end{array}",
#     r"\begin{array} { l } 4 x ^ { 2 } + y ^ { 2 } = 4 \\ y = x + 2 \end{array}",
#     r"\begin{array} { l } x ^ { 2 } + 9 y ^ { 2 } = 9 \\ y = \frac { 1 } { 3 } x - 3 \end{array}",
#     r"\begin{array} { l } 9 x ^ { 2 } + y ^ { 2 } = 9 \\ y = 3 x - 3 \end{array}",
#     r"\begin{array} { l } y = 4 \\ ( x - 2 ) ^ { 2 } + ( y + 3 ) ^ { 2 } = 4 \end{array}",
#     r"\begin{array} { l } x = - 6 \\ ( x + 3 ) ^ { 2 } + ( y - 1 ) ^ { 2 } = 9 \end{array}",
    # r"\begin{array} { l } a + b + c = 10 \\ a b + a c + b c = 50 \\ a ^ { 2 } + b ^ { 2 } + c ^ { 2 } = 100 \end{array}",
    # r"\begin{array} x^2 + y^2 & = 10 \\ xy & = + 50 \end{array}",
    # r"x + 2y + 3z = -6, 2x + 3y + 4z = 10, 3x + 4y + 5z = 14",
    # r"a - b = -c",
    # r"p - q - r = -s, m + n + o = 7, i + j + k = -l",
    # r"( a - b ) ^ { 2 }",
    # r"x ^ { 2 } + 4 x + 6 = 0",
    # r"x ^ { 3 } + x ^ { 2 } y + x y ^ { 2 } + y ^ { 3 }",
    # r"a x ^ { 2 } + b x + c = 0",
    # r"\frac { ( x ^ { 2 } - 1 ) } { ( x ^ { 2 } + 1 ) }",
    # r"10 - 9 + 8 - 7 + 6 - 5 + 4 - 3 + 2 - 2",
    # r"\sqrt { ( 3 ^ { 2 } + 4 ^ { 2 } ) }",
    # r"\int x ^ { 2 } \sin ^ { 3 } x d x",
    # r"\frac { d } { d x } ( x ^ { 4 } \sin x )",
    # r"\cos ( x ) + \frac { 1 } { 2 } \cos ( 2 x ) + \frac { 1 } { 4 } \cos ( 4 x )",
    # r"\sin ( \frac { \pi } { 5 } )",
    # r"\cot ^ { - 1 } ( x )",
    # r"\sin ( x + y + z )",
    # # r"y ^ { \prime \prime } + y = 0",
    # # r"y ^ { \prime \prime } ( z ) + \sin ( y ( z ) ) = 0",
    # r"x ^ { 2 } - 2 y ^ { 2 } = 1",
    # r"y = \sin ( x ) \times \cos ( 3 x )",
    # r"4 ^ { x - 1 } = 4 ^ { 3 }",
    # r"3 ^ { k - 7 } = 9 ^ { 3 - x }",
    # r"5 ^ { 5 x + 2 } = 30",
    # r"x^2 - 3x - 10 = 0",   
    # r"\frac{36 a^{12} b^7}{54 a^8 b^{11}}",
    # r"\frac{3 a}{a^2+a b}-\frac{5 a-3 b^2}{a^2-b^2}",
    # r"2x + 3y = 8",
    # r"3a - 5b + 2c = 12",
    # r"x^2 + 3y = 7",
    # r"a^2 + b^2 - c^2 = 25",
    # r"2x + 3y = 8, 4x - y = 6",
    # r"3a - 5b + 2c = 12, a + 2b - 4c = 7, 2a + 4b + c = 15",
    # r"x^2 + 3y = 7, 2x - y^2 = 1",
    # r"a^2 + b^2 - c^2 = 25, 3a + 2b + c^2 = 17, a^2 + 2b - 4c = 5",
    # r"x^2 - 3x - 10 = 0",
    # r"x^2 - 5x + 6 = 0",
    # r"9125 + 1000",
    # r"1/(1+\sqrt{2})",
    # r"\sin(x) + \cos(x) = 1",
    # r"\log_2(x) = 3",
    # r"2^x = 16",
    # r"3x^3 + 2x^2 - 5x + 1 = 0",
    # r"\frac{1}{x+2} = \frac{3}{x-1}",
    # r"2x - 3 = 5",
    # r"\sqrt{x+2} = 4",
    # r"2x + 3i = 1 - 4i",
    # r"2x + y = 5",
    # r"3x - 2y = 1",
    # r"2x + 3 = 7",
    # r"x^3 - 4x^2 + 5x - 2 = 0",
    # r"\frac{a}{b} + \frac{c}{d} = \frac{e}{f}",
    # r"\sqrt{16} = 4",
    # r"\int_0^1 x^2 dx",
    # r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}",
    # r"\lim_{x \to 0} \frac{\sin(x)}{x} = 1",
    # r"e^{i\pi} + 1 = 0",
    # r"F = m \cdot a",
    # r"\binom{n}{k} = \frac{n!}{k!(n-k)!}",
    # r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
    # r"\text{Einstein's mass-energy equivalence: } E=mc^2",
    # r"\frac{d^2 \psi}{dx^2} + k^2\psi = 0",
    # r"\frac{dy}{dx} = ky",
    # r"\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})",
    # r"x_{n+1} = rx_n(1 - x_n)",
    # r"\oint_C \vec{F} \cdot d\vec{r} = \iint_S (\nabla \times \vec{F}) \cdot d\vec{S}",
    # r"\sqrt{\frac{a+b}{c}}",
    # r"\sin^2(x) + \cos^2(x) = 1",
    # r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u",
    # r"\left(\frac{a}{b}\right)^3",
    # r"\sum_{k=0}^{n} {n \choose k} a^k (1-a)^{n-k}",
    # r"\lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x = e",
    # r"\frac{d^2\theta}{dt^2} + \frac{g}{l}\sin(\theta) = 0",
    # r"\begin{aligned} x + 2 y + 3 z & = 6 \\ 2 x + 3 y + 4 z & = 10 \\ 3 x + 4 y + 5 z & = 14 \end{aligned}",
    # Add more examples here
# ]

comma_separated_list_of_equations = []

# print('*->', latex_systems)
# for latex_system in latex_systems:
comma_separated_equation = convert_latex_system_to_comma_separated_list(latex_systems)
comma_separated_list_of_equations.append(comma_separated_equation)

# for eq in comma_separated_list_of_equations:
#     print(eq)
#     exit()


def extract_variables_from_formula(formula):
    names = [i.id for i in ast.walk(ast.parse(formula)) if isinstance(i, ast.Name)]
    return list(set(names))

def replace_equals_sign(match):
    if match.group(1) == '=':
        return '-'
    
modified_equations_if = []
modified_equations_else = []


for equations_set in comma_separated_list_of_equations:
    if re.search(r',', equations_set):
        if re.search(r'=|=', equations_set):
            equations_set1 = add_parentheses_to_equations(equations_set)
            equations_set = re.sub(r'(=)|=', replace_equals_sign, equations_set1)
        modified_equations_if.append(equations_set)
    else:
        modified_equations_else.append(equations_set)

print('input->', modified_equations_if)
print('input->', modified_equations_else)
# # for eq in 
# print(modified_equations_if)
# exit()


results = []
# Print equations with replacements (if)
for modified_equation in modified_equations_if:
    result = {}
    sympy_expr = latex2sympy(modified_equation)
    print(sympy_expr)
    # print(sympy_expr)
    exit()
    result["Input"] = sympy_expr
    # result["Sympy Output"] = sympy_expr
    
    variables = extract_variables_from_formula(str(sympy_expr))
    
    pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

    # Filter the variables to keep only single alphabets
    filtered_variables = [var for var in variables if re.match(pattern, var)]
    # print(filtered_variables)

    variables = tuple(filtered_variables)
    try:
        solutions = solve_with_timeout(sympy_expr, list(variables))
        print('outputlatex', latex(solutions))
        solution2 = pprint(solutions, use_unicode=True)
        result["Output"] = solutions
    except TimeoutError:
        print('The equation took too long to solve.')
        result["Output"] = "Solving time exceeded"
        
    
    
    results.append(result)
    
    
# Print original equations (else)
for original_equation in modified_equations_else:
    result = {}
    # print("single equations---------->", original_equation)
    result["Input"] = original_equation
    try:
        print('output->', latex2latex(original_equation))
                
        # result["Input"] = latex2latex(original_equation)
        result["Output"] = latex2latex(original_equation)
    except Exception as e:
        print('output->', "Equation not solvable")
        
        result["Output"] = "Equation not solvable"
    
    
    results.append(result)
    

# # Save results to a CSV file
# with open('./result_system_new.csv', 'w', newline='') as csvfile:
#     fieldnames = ["Input", "Output"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     for result in results:
#         writer.writerow(result)

# print("Results saved to 'result_system_new.csv'")  