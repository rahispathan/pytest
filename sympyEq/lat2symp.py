import re

def replace_equals_sign(match):
    if match.group(1) == '&= -':
        return '+'
    else:
        return '-'

def convert_latex_system_to_comma_separated_list(latex_system):
    """This function converts a LaTeX system of equations to a comma-separated list of equations."""
    
    # Regular expression pattern to match a LaTeX system of equations.
    latex_system_pattern = r"\\begin{system}(.*?)\\end{system}"
    
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
        if re.search(r'&= -|&=', equation):
            comma_separated_equations.append(re.sub(r'(&= -)|&=', replace_equals_sign, equation))
    
    # Join the modified equations back together using the comma as the delimiter.
    comma_separated_list_of_equations = ",".join(comma_separated_equations)
    
    return comma_separated_list_of_equations

# Example usage:
latex_systems = [
    r"\begin{system} x + y &= 10 \\ xy + xz + yz &= 50 \\ x^3 + y^3 + z^3 &= - 100 \end{system}",
    r"\begin{system} a + b + c &= 10 \\ ab + ac + bc &= 50 \\ a^2 + b^2 + c^2 &= 100 \end{system}",
    r"\begin{system} x^2 + y^2 &= 10 \\ xy &= - 50 \end{system}",
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
    # Add more examples here
]

comma_separated_list_of_equations = []

for latex_system in latex_systems:
    comma_separated_equation = convert_latex_system_to_comma_separated_list(latex_system)
    comma_separated_list_of_equations.append(comma_separated_equation)

# Print the comma-separated list of equations.
for eq in comma_separated_list_of_equations:
    print(eq)