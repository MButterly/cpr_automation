import fitz  # PyMuPDF

# Open the PDF
pdf_path = 'input.pdf'
doc = fitz.open(pdf_path)

# List of student names and positions (page_number, x, y, name)
students = [
    (0, 100, 100, "Student Name 1"),
    (0, 100, 150, "Student Name 2"),
    # Add more as needed
]

# Add text to specified positions
for page_num, x, y, name in students:
    page = doc.load_page(page_num)
    page.insert_text((x, y), name, fontsize=12, color=(0, 0, 0))  # Adjust fontsize and color

# Save the updated PDF
doc.save("output.pdf")
doc.close()
