from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors

# Define the page size
page_width, page_height = 800, 600  # Adjust the width and height as needed
pagesize = (page_width, page_height)

# Your list of equations and corresponding solution PNG image paths
equations = ["3x - 5 > -2(x - 10)", 
             "x^2 - 3x - 10 = 0", 
             "(36a^12b^12)/(54a^8b^11)", 
             "(3a)/(a^2 + ab) - (5a - 3b^2)/(a^2 - b^2)",
             "sin(x) + cos(x) = 1",
             "2x + 3i = 1 - 4i",
             "(a/b) + (c/d) = (e/f)",
             "x^3 - 4x^2 + 5x - 2 = 0",
             ]
 
# solution_images = ["../result_1.png", "../result_2.png", "../result_4.png", "../result_5.png", "../result_8.png", "../result_14.png", "../result_19.png", "../result_18.png"]

# Create a PDF document
doc = SimpleDocTemplate("equations.pdf", pagesize=letter)  # Set the custom page size

# Create a list to store table data
data = [["Equation", "Solution"]]

# Add equations and solutions to the table
for i, equation in enumerate(equations):
    # equation_image = Image(solution_images[i], width=50, height=10)  # Adjust width and height as needed
    data.append([equation])

# Create the table
table = Table(data, colWidths=[300, 450])

# Add style to the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

table.setStyle(style)

# Build the PDF document
doc.build([table])