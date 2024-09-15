import fitz  # PyMuPDF
import pandas as pd
import sys 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_path>")
        sys.exit(1)

    # Get course data from the user
    course_date = input("What was the date of the class? ")
    course_type = input("What type of course was it (BLS/HSFA/HSCPR)? ")

    # Open the PDF
    if course_type == "BLS":
        pdf_path = 'PDFs/Adult_BLS.pdf'
    elif course_type == "HSFA":
        pdf_path = 'PDFs/HSFA.pdf'
    elif course_type == "HSCPR":
        pdf_path = 'PDSs/HSCPR.pdf'
    else:
        print("Error in choosing PDF")
        sys.exit(2)
    doc = fitz.open(pdf_path)

    # Create the pandas dataframe
    csv_path = sys.argv[2]
    df = pd.read_csv(csv_path)
    
    # Combine 'First Name' and 'Last Name' into a 'Full Name' column
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']


    # # Loop through each row in the DataFrame and add text to the specified positions
    # for index, row in df.iterrows():
    #     name = row['name']
        
    # # Add text to specified positions
    # for name in students:
    #     page = doc.load_page(0)
    #     page.insert_text((100, 100), name, fontsize=12, color=(0, 0, 0))  # 100,100 indicates the location of the text insertion

    print ('works after pandas')

    # Save the updated PDF
    doc.save("output.pdf")
    doc.close()

    # Create a roster