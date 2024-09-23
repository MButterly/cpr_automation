import fitz  # PyMuPDF
import pandas as pd
import sys 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_path>")
        sys.exit(1)

    # Get course data from the user
    course_date = input("What was the date of the class? ")
    course_type = input("What type of course was it (BLS/HSFACPR)? ")

    # Create roster for the class
    if course_type == "BLS":
        roster_output = fitz.open('BLS_Roster.pdf')
    elif course_type == "HSFACPR":
        roster_output = fitz.open('HSFACPR_Roster.pdf')
    else:
        print("Error in choosing Roster PDF")
        sys.exit(2)

    # Open the skillsheet PDFs
    # Create a doc to hold the outputs
    output_skill_doc = fitz.open()

    if course_type == "BLS":
        template_doc = 'PDFs/Adult_BLS.pdf'
    elif course_type == "HSFACPR":
        template_doc = 'PDFs/HSFACPR.pdf'
    else:
        print("Error in choosing skillsheet PDF")
        sys.exit(2)
    template_skill_doc = fitz.open(template_doc)

    # Add the date to the template
    template_skill_doc.insert_text((500, 100), course_date, fontsize=12, color=(0, 0, 0))

    # Create the pandas dataframe
    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)
    
    # Combine 'First Name' and 'Last Name' into a 'Full Name' column
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']

    # Loop through each row in the DataFrame and add text to the specified positions
    for index, row in df.iterrows():
        name = row['Full Name']

        # Add text to specified positions. Keep an eye on the correct coordinates
        filled_skill_sheet = template_skill_doc.load_page(0)
        filled_skill_sheet.insert_text((100, 100), name, fontsize=12, color=(0, 0, 0))

        # Append the data to the growing output PDF
        # Maybe this will work, maybe it won't
        output_skill_doc.insert_pdf(filled_skill_sheet, from_page=0)

        # Add the name to the roster
        roster_output.insert_text((100,(index*100)+200), name, fontsize=12, color=(0,0,0))
 
    # Save & close the skillsheet output
    output_skill_doc.save('Skillsheets_for_' + course_type)
    output_skill_doc.close()

    # Save & close the roster output
    roster_output.save('Roster_for_' + course_type)
    roster_output.close()

    print("Don't forget to fill out the rest of the roster!")
    print("Did you want to alphabetize the names in the roster?")