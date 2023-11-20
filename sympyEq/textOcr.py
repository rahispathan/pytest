import re

# Modify the function to add parentheses around the right-hand side
def add_parentheses(match):
    return f'{match.group(1)} = ({match.group(2)})'

def add_parentheses_to_equations(equations):
    # Define a regular expression pattern to find equations with '=' sign
    equation_pattern = re.compile(r'(\S+)\s*=\s*(.*?)(?:,|$)', re.M)

    # Use the pattern to add parentheses to the right-hand side of equations
    equations_with_parentheses = equation_pattern.sub(add_parentheses, equations)
    
    return equations_with_parentheses

# Test with example equations
equations = r"\begin{system} x + y &= 10 \\ xy + xz + yz &= 50 \\ x^3 + y^3 + z^3 &= - 100 \end{system}"

equations_with_parentheses = add_parentheses_to_equations(equations)

print(equations_with_parentheses)