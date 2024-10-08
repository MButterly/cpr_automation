import fitz  # PyMuPDF
import pandas as pd
import sys 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_path>")
        sys.exit(1)

    # Get course data from the user
    course_location = input("What was the course's address? ")
    course_type = input("What type of course was it (BLS/HS)? ")

    # Create roster for the class
    if course_type == "BLS":
        roster_output = fitz.open('PDFs/BLS-Roster.pdf')
    elif course_type == "HS":
        roster_output = fitz.open('PDFs/HSFACPR-Roster.pdf')
    else:
        print("Error in choosing Roster PDF")
        sys.exit(2)

    # Open the skillsheet PDFs
    # Create a doc to hold the skillsheet outputs
    output_skill_doc = fitz.open()

    if course_type == "BLS":
        template_doc = 'PDFs/Adult_BLS.pdf'
    elif course_type == "HS":
        template_doc = 'PDFs/HSFACPR-Skills-CPR.pdf'
        fa_template_doc = 'PDFs/HSFACPR-Skills-FA.pdf'
    else:
        print("Error in choosing skillsheet PDF")
        sys.exit(2)

    # Create the pandas dataframe and alphabetize by last name
    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)
    df.sort_values('Last Name', inplace=True)
    
    # Combine 'First Name' and 'Last Name' into a 'Full Name' column
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']

    # Loop through each row in the DataFrame and add text to the specified positions
    for index, row in df.iterrows():
        name = row['Full Name']
        email = row['Email']
        course_date = row['Course Date']

        # Add name and course date to their respective locations on form
        filled_skill_doc = fitz.open(template_doc)
        filled_skill_page = filled_skill_doc.load_page(0)
        filled_skill_page.insert_text((450, 110), course_date, fontsize=12, color=(0, 0, 0))
        filled_skill_page.insert_text((450, 685), course_date, fontsize=12, color=(0, 0, 0))
        filled_skill_page.insert_text((125, 110), name, fontsize=12, color=(0, 0, 0))

        output_skill_doc.insert_pdf(filled_skill_doc)

        # If First Aid course, add FA skillsheet and fill it out
        if course_type == 'HS':
            filled_fa_skill_doc = fitz.open(fa_template_doc)
            filled_fa_skill_page = filled_fa_skill_doc.load_page(0)
            filled_fa_skill_page.insert_text((450, 110), course_date, fontsize=12, color=(0, 0, 0))
            filled_fa_skill_page.insert_text((450, 695), course_date, fontsize=12, color=(0, 0, 0))
            filled_fa_skill_page.insert_text((125, 110), name, fontsize=12, color=(0, 0, 0))   

            output_skill_doc.insert_pdf(filled_fa_skill_doc)

        # Add info to the roster
        roster_page = roster_output.load_page(1)
        y_position = 175 + index * 41 # This will be determined experimentally
        roster_page.insert_text((80, y_position), name, fontsize=12, color=(0, 0, 0))
        roster_page.insert_text((80, y_position + 20), email, fontsize=12, color=(0, 0, 0))
        roster_page.insert_text((325, y_position), course_location, fontsize=12, color=(0, 0, 0))
        roster_page.insert_text((625, y_position + 10), 'C', fontsize=30, color=(0, 0, 0))

    # Save & close the skillsheet output
    output_skill_doc.save('Skillsheets_for_' + course_type + '.pdf')
    output_skill_doc.close()

    # Save & close the roster output
    roster_output.save('Roster_for_' + course_type + '.pdf')
    roster_output.close()

    print("Don't forget to fill out the rest of the roster!")