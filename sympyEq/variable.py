# import ast
# import re
import csv

# # formula = 'a = b3*2*C2'           # get the formula as a string
# # formula = 'x**2-3*x-10'

# def extract_variables_from_formula(formula):
#     names = [i.id for i in ast.walk(ast.parse(formula)) if isinstance(i, ast.Name)]
#     return list(set(names))


# formulas = [
#     "[Eq(x, 1/2 - 7*i/2), Eq(i, 1/7 - 2*x/7)]",
#     "3*x - 5 > -1*2*(x - 10)",
#     "[Eq(x, -2), Eq(x, 5)]",
#     "1000 + 9125",
#     "(36*a**12*b**7)/((54*a**8*b**11))",
#     "(3*a)/(a**2 + a*b) - (5*a - 1*3*b**2)/(a**2 - b**2)",
#     "1/(1 + sqrt(2))",
#     "[Eq(x, 2), Eq(x, 3)]",
#     "[Eq(x, 0), Eq(x, pi/2)]",
#     "[Eq(x, 8)]",
#     "[Eq(x, 4)]",
#     "[Eq(x, -7/2)]",
#     "[Eq(x, 4)]",
#     "[Eq(x, 14)]",
#     "[Eq(x, 1/2 - 7*i/2), Eq(i, 1/7 - 2*x/7)]",
#     "[Eq(y, 5 - 2*x), Eq(x, 5/2 - y/2)]",
#     "[Eq(x, 2*y/3 + 1/3), Eq(y, 3*x/2 - 1/2)]",
#     "[Eq(x, 2)]",
#     "[Eq(x, 1), Eq(x, 2)]",
#     "[Eq(c, -a*d/b + E*d/f), Eq(b, -a*d*f/(c*f - E*d)), Eq(f, E*b*d/(a*d + b*c)), Eq(a, -b*c/d + E*b/f), Eq(d, -b*c*f/(a*f - E*b))]",
#     "Eq(sqrt(16), 4)",
#     "Integral(x**2, (x, 0, 1))",
#     "[Eq(n, -sqrt(8*Sum(i, (i, 1, n)) + 1)/2 - 1/2), Eq(n, sqrt(8*Sum(i, (i, 1, n)) + 1)/2 - 1/2)]",
#     "[Eq(i, I)]",
#     "a*m",
#     "a = b*2*C2",
#     "\frac{d^2\theta}{dt^2} + \frac{g}{l}\sin(\theta) = 0"
# ]

# result = []

# for formula in formulas:
    
#     variables = extract_variables_from_formula(formula)

#     # Regular expression to match single alphabets
#     pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

#     # Filter the variables to keep only single alphabets
#     filtered_variables = [var for var in variables if re.match(pattern, var)]

#     result.append([formula, ', '.join(variables), ', '.join(filtered_variables)])

# # Write the results to a CSV file
# with open('formula_results.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Formula', 'Variables', 'Filtered Variables'])
#     writer.writerows(result)
from latex2sympy2 import latex2sympy, latex2latex
from sympy import symbols, solve, simplify, preview, sympify, nsolve
import ast
import re

equations_input = [
    r"x^2 + y^2 - 10 , xy - 5 ",
    r"x^3 + y^3 + z^3 - 100 , xy + xz + yz - 50 , x^2 + y^2 + z^2 - 100",
    r"x + y - 10 , xy + xz + yz - 50 , x^3 + y^3 + z^3 + 100",
    r"a + b + c - 10 , ab + ac + bc - 50 , a^2 + b^2 + c^2 - 100",
    r"x^2 + y^2 - 10 , xy - 50",
    r"x + 2y + 3z = -6, 2x + 3y + 4z = 10, 3x + 4y + 5z = 14",
    r"a - b = -c",
    r"p - q - r = -s, m + n + o = 7, i + j + k = -l",
    r"( a - b ) ^ { 2 }",
    r"x ^ { 2 } + 4 x + 6 = 0",
    r"x ^ { 3 } + x ^ { 2 } y + x y ^ { 2 } + y ^ { 3 }",
    r"a x ^ { 2 } + b x + c = 0",
    r"\frac { ( x ^ { 2 } - 1 ) } { ( x ^ { 2 } + 1 ) }",
    r"10 - 9 + 8 - 7 + 6 - 5 + 4 - 3 + 2 - 2",
    r"\sqrt { ( 3 ^ { 2 } + 4 ^ { 2 } ) }",
    r"\int x ^ { 2 } \sin ^ { 3 } x d x",
    r"\frac { d } { d x } ( x ^ { 4 } \sin x )",
    r"\cos ( x ) + \frac { 1 } { 2 } \cos ( 2 x ) + \frac { 1 } { 4 } \cos ( 4 x )",
    r"\sin ( \frac { \pi } { 5 } )",
    r"\cot ^ { - 1 } ( x )",
    r"\sin ( x + y + z )",
    # r"y ^ { \prime \prime } + y = 0",
    # r"y ^ { \prime \prime } ( z ) + \sin ( y ( z ) ) = 0",
    r"x ^ { 2 } - 2 y ^ { 2 } = 1",
    r"y = \sin ( x ) \times \cos ( 3 x )",
    r"4 ^ { x - 1 } = 4 ^ { 3 }",
    r"3 ^ { k - 7 } = 9 ^ { 3 - x }",
    r"5 ^ { 5 x + 2 } = 30",
    r"x^2 - 3x - 10 = 0",   
    r"\frac{36 a^{12} b^7}{54 a^8 b^{11}}",
    r"\frac{3 a}{a^2+a b}-\frac{5 a-3 b^2}{a^2-b^2}",
    r"2x + 3y = 8",
    r"3a - 5b + 2c = 12",
    r"x^2 + 3y = 7",
    r"a^2 + b^2 - c^2 = 25",
    r"2x + 3y = 8, 4x - y = 6",
    r"3a - 5b + 2c = 12, a + 2b - 4c = 7, 2a + 4b + c = 15",
    r"x^2 + 3y = 7, 2x - y^2 = 1",
    r"a^2 + b^2 - c^2 = 25, 3a + 2b + c^2 = 17, a^2 + 2b - 4c = 5",
    r"x^2 - 3x - 10 = 0",
    r"x^2 - 5x + 6 = 0",
    r"9125 + 1000",
    r"1/(1+\sqrt{2})",
    r"\sin(x) + \cos(x) = 1",
    r"\log_2(x) = 3",
    r"2^x = 16",
    r"3x^3 + 2x^2 - 5x + 1 = 0",
    r"\frac{1}{x+2} = \frac{3}{x-1}",
    r"2x - 3 = 5",
    r"\sqrt{x+2} = 4",
    r"2x + 3i = 1 - 4i",
    r"2x + y = 5",
    r"3x - 2y = 1",
    r"2x + 3 = 7",
    r"x^3 - 4x^2 + 5x - 2 = 0",
    r"\frac{a}{b} + \frac{c}{d} = \frac{e}{f}",
    r"\sqrt{16} = 4",
    r"\int_0^1 x^2 dx",
    r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}",
    r"\lim_{x \to 0} \frac{\sin(x)}{x} = 1",
    r"e^{i\pi} + 1 = 0",
    r"F = m \cdot a",
    r"\binom{n}{k} = \frac{n!}{k!(n-k)!}",
    r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
    r"\text{Einstein's mass-energy equivalence: } E=mc^2",
    r"\frac{d^2 \psi}{dx^2} + k^2\psi = 0",
    r"\frac{dy}{dx} = ky",
    r"\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})",
    r"x_{n+1} = rx_n(1 - x_n)",
    r"\oint_C \vec{F} \cdot d\vec{r} = \iint_S (\nabla \times \vec{F}) \cdot d\vec{S}",
    r"\sqrt{\frac{a+b}{c}}",
    r"\sin^2(x) + \cos^2(x) = 1",
    r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u",
    r"\left(\frac{a}{b}\right)^3",
    r"\sum_{k=0}^{n} {n \choose k} a^k (1-a)^{n-k}",
    r"\lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x = e",
    r"\frac{d^2\theta}{dt^2} + \frac{g}{l}\sin(\theta) = 0",
]

def extract_variables_from_formula(formula):
    names = [i.id for i in ast.walk(ast.parse(formula)) if isinstance(i, ast.Name)]
    return list(set(names))

def replace_equals_sign(match):
    if match.group(1) == '= -':
        return '+'
    else:
        return '-'
    
modified_equations_if = []
modified_equations_else = []

for equations_set in equations_input:
    if re.search(r', ', equations_set):
        if re.search(r'= -|=', equations_set):
            equations_set = re.sub(r'(= -)|=', replace_equals_sign, equations_set)
        modified_equations_if.append(equations_set)
    else:
        modified_equations_else.append(equations_set)

results = []
# Print equations with replacements (if)
for modified_equation in modified_equations_if:
    result = {}
    sympy_expr = latex2sympy(modified_equation)
    result["Input"] = sympy_expr
    # result["Sympy Output"] = sympy_expr
    
    variables = extract_variables_from_formula(str(sympy_expr))
    
    pattern = r'^(?![a-zA-Z]+$)[a-zA-Z0-9_]+$|^[a-zA-Z]$'

    # Filter the variables to keep only single alphabets
    filtered_variables = [var for var in variables if re.match(pattern, var)]
    # print(filtered_variables)

    variables = tuple(filtered_variables)
    # print(variables)
    # exit()
    
    solutions = solve(sympy_expr, list(variables), dict=True)
    
    result["Output"] = solutions
    
    results.append(result)
    
    

# Print original equations (else)
for original_equation in modified_equations_else:
    result = {}
    # print("single equations---------->", original_equation)
    result["Input"] = original_equation
    try:
        # result["Input"] = latex2latex(original_equation)
        result["Output"] = latex2latex(original_equation)
    except Exception as e:
        result["Output"] = "Equation not solvable"
    
    results.append(result)
    
        

# Save results to a CSV file
with open('./result_28_new.csv', 'w', newline='') as csvfile:
    fieldnames = ["Input", "Output"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for result in results:
        writer.writerow(result)

print("Results saved to 'result_28_new.csv'")
    