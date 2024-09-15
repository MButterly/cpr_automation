import fitz  # PyMuPDF
import pandas as pd
import sys 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_path> <Date_of_Class>")
        sys.exit(1)

    # Open the PDF
    pdf_path = 'PDFs/Adult_BLS.pdf'
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

    # Save the updated PDF
    doc.save("output.pdf")
    doc.close()
