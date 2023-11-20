import csv
import ast
import re
from latex2sympy2 import latex2sympy, latex2latex
from sympy import symbols, solve, simplify, preview, sympify, nsolve
from IPython.display import display, Math
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)

# Define symbols
# x = symbols('x')
# a, b, c = symbols('a b c')


def extract_variables_from_formula(formula):
    names = [i.id for i in ast.walk(ast.parse(formula)) if isinstance(i, ast.Name)]
    return list(set(names))
    
# List of LaTeX expressions
latex_expressions = [
    r"& x+2 y+3 z=6 \\
& 2 x+3 y+4 z=10",
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
    # r"y ^ { \prime \prime } + y = 0",
    # r"y ^ { \prime \prime } ( z ) + \sin ( y ( z ) ) = 0",
    # r"x ^ { 2 } - 2 y ^ { 2 } = 1",
    # r"y = \sin ( x ) \times \cos ( 3 x )",
    # r"4 ^ { x - 1 } = 4 ^ { 3 }",
    # r"3 ^ { k - 7 } = 9 ^ { 3 - x }",
    # r"5 ^ { 5 x + 2 } = 30"
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
    # r"\vec{F} = \frac{d\vec{p}}{dt}",
    # r"\frac{d^2y}{dx^2} = -k^2y",
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
    
]

results = []

# for latex_expr in latex_expressions:
    
#     print('asdv----', parse_expr("10sin**2 x**2 + 3xyz + tan theta", transformations=(standard_transformations + (implicit_multiplication_application,))))
#     sympy_expr = latex2sympy(latex_expr)
    
#     variables = extract_variables_from_formula(str(sympy_expr))
    
#     pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

#     # Filter the variables to keep only single alphabets
#     filtered_variables = [var for var in variables if re.match(pattern, var)]
    
#     x, y, z = symbols(tuple(filtered_variables))
    
#     solutions = solve([x + 2*y + 3*z - 6, 2*x + 3*y + 4*z - 10, 3*x + 4*y + 5*z - 14], tuple(filtered_variables))
    
#     print('vars--------', filtered_variables)
# print('sympy_expr--------', "x + 2*y + 3*z = 6, 2*x + 3*y + 4*z = 10, 3*x + 4*y + 5*z = 14")
#     print('solve---', solutions)
#     print()


#     # Regular expression to match single alphabets
#     pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

#      Filter the variables to keep only single alphabets
#     filtered_variables = [var for var in variables if re.match(pattern, var)]

#     result.append([formula, ', '.join(variables), ', '.join(filtered_variables)])

#  Write the results to a CSV file
# with open('formula_results.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Formula', 'Variables', 'Filtered Variables'])
#     writer.writerows(result)


# result = {}  # Store results


for latex_expr in latex_expressions:
    result = {}

    try:
        result["Original LaTeX"] = latex_expr
        result["latex2sympy -> l2s2"] = str(latex2sympy(latex_expr))
        print(result["latex2sympy -> l2s2"])
        exit
        result["l2l -> l2s2"] = latex2latex(latex_expr)

    # Convert LaTeX to SymPy
        sympy_expr = latex2sympy(latex_expr)

        if sympy_expr is not None:
        # Check if the equation is solvable
            # Attempt to solve the expression
            x, y, z = symbols('x y z')  # Define symbols here
            solutions = solve([sympy_expr], (x, y, z))  # Include all the variables here

            # Simplify the expression
            simplified_expr = simplify(sympy_expr)

            # Add results to the dictionary
            result["SymPy Expression -> sympy"] = str(sympy_expr)
            result["Simplified Expression -> sympy"] = str(simplified_expr)
            result["Solutions -> sympy"] = str(solutions)
        else:
            # LaTeX to SymPy conversion failed
            result["SymPy Expression -> sympy"] = "Conversion Failed"
            result["Simplified Expression -> sympy"] = "Conversion Failed"
            result["Solutions -> sympy"] = "Conversion Failed"

    except Exception as e:
        # Equation is not solvable
        result["SymPy Expression -> sympy"] = "Not Solvable"
        result["Simplified Expression -> sympy"] = "Not Solvable"
        result["Solutions -> sympy"] = "Not Solvable"
    results.append(result)
    
print(results)

# Save results to a CSV file
with open('./result_27.csv', 'w', newline='') as csvfile:
    fieldnames = ["Original LaTeX", "latex2sympy -> l2s2", "l2l -> l2s2", "SymPy Expression -> sympy", "Simplified Expression -> sympy", "Solutions -> sympy"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for result in results:
        writer.writerow(result)

print("Results saved to 'result_27.csv'")