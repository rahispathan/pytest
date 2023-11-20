from sympy import symbols, Eq, solve

# Define symbols
x = symbols('x')

# Define the equation
eq = Eq(x**2 - 3*x - 10, 0)

# List to store intermediate steps
steps = []

# Step 1: Define the equation
steps.append("Step 1: Define the equation")
steps.append(str(eq))

# Step 2: Solve the equation
solutions = solve(eq, x)
steps.append("\nStep 2: Solve the equation")
for i, solution in enumerate(solutions):
    steps.append(f"Solution {i + 1}: x = {solution}")

# Save the steps to a text file
with open('sympyEq/solution_steps.txt', 'w') as file:
    for step in steps:
        file.write(step + '\n')

print("Solution steps saved to 'sympyEq/solution_steps.txt'")