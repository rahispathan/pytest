from pyparsing import Word, alphas

# List of equations
equations = [r"3x-5>-2(x-10)",
    r"\frac{36 a^{12} b^7}{54 a^8 b^{11}}",
    r"\frac{3 a}{a^2+a b}-\frac{5 a-3 b^2}{a^2-b^2}",
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
    r"\vec{F} = \frac{d\vec{p}}{dt}",
    r"\frac{d^2y}{dx^2} = -k^2y",
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
    r"2x + 3y = 8",
    r"3a - 5b + 2c = 12",
    r"x^2 + 3y = 7",
    r"a^2 + b^2 - c^2 = 25",
    r"2x + 3y = 8, 4x - y = 6",
    r"3a - 5b + 2c = 12, a + 2b - 4c = 7, 2a + 4b + c = 15",
    r"x^2 + 3y = 7, 2x - y^2 = 1",
    r"a^2 + b^2 - c^2 = 25, 3a + 2b + c^2 = 17, a^2 + 2b - 4c = 5",    
]

# Define the variable parsing logic
variable = Word(alphas, min=1)

# Loop through the equations and parse variables
for equation in equations:
    variables = variable.searchString(equation)
    variables_list = variables.asList()
    print(f"Equation: {equation}")
    print(f"Variables: {variables_list}")
    print()