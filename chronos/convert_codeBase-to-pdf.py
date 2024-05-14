"""
File Name: convert_codeBase-to-pdf.py
Description: This python script automates the process of converting a codebase into a PDF document.
Author: Beau Magnum
Date: 05/12/2024

Functionality:

* Fetches the latest files from the GitHub repository.
* Extracts filenames and orders them based on the structure defined in codeBase-list.md.
* Utilizes Pandoc to convert the Markdown files into a single, well-structured PDF.
* Uploads the generated PDF to Google Drive.

**Benefits:**

* Give's AI A single place to review the entire codebase from so that it can offer improvements and suggestions.
* Ensures consistency in formatting and presentation.

**Instructions:**

1. Configure the script with your GitHub repository details and Google Drive credentials.
2. Run the script to generate and upload the PDF.

Date Last Updated: 05/12/2024

"""

import os 
import re # Allows python to use regular expressions for pattern matching. In this case, we use it to extract filenames from the 'codeBase-list.md' file
import sys # Allows python to interact with the system, in this case, we use it to access command-line arguments
import subprocess # Allows python to execute external commands, in this case, we use it to pull the latest codebase from GitHub
from reportlab.lib.styles import getSampleStyleSheet # Allows python to use the default styles for the PDF
from reportlab.pdfgen import canvas # Allows python to generate a PDF file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer # Allows python to create a simple document template, paragraphs, and space in the PDF
from Security.all_access import get_system_username, get_chronos_directory_structure  # Importing the all_access.py file from the Security folder. Which has personal details from the user

# --- Git pull for updating codebase on local computer ---
def get_latest_codebase_content(local_codebase_directory):
    
    # Determine what computer the user is using by the system username
    username = get_system_username() # function located inside 'all_access.py' file, needed to access the user's home directory

    os.chdir(local_codebase_directory) # Change directory to the codebase location
    try:
        subprocess.run(["git", "pull"], check=True) # Run the git pull command to update the codebase on the local computer
    except subprocess.CalledProcessError as e:
        print(f"Error updating codebase: {e}") # Print an error message if the git pull command fails
        
def extract_filenames_from_codebase_list(local_codebase_directory):
    file_list = []
    link_pattern = re.compile(r'\s*\[.*\]\((.*)\)')  # Extracts the filename from a Markdown link, in this case '[Display_Text](filename)'
    
    with open(os.path.join(local_codebase_directory, 'codeBase-list.md'), 'r') as file: # Open the 'codeBase-list.md' file in read mode
        for line in file:
            match = link_pattern.search(line) # Check if the line matches the link pattern
            if match:
                file_list.append(match.group(1)) # If there is a match, extract the filename and add it to the list
    return file_list # Return the list of filenames extracted from the 'codeBase-list.md' file

def convert_code_to_pdf(file_paths, output_pdf, local_codebase_directory):
    doc = SimpleDocTemplate(output_pdf, pagesize=(1500, 3600), leftMargin=50)
    story = []
    styles = getSampleStyleSheet()
    code_style = styles['Code']

    for file_path in file_paths:
        full_path = os.path.join(local_codebase_directory, file_path)
        with open(full_path, 'r') as file:
            content = file.read()
        
        story.append(Paragraph(f"File: {full_path}", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        preformatted_text = Preformatted(content, code_style)
        story.append(preformatted_text)
        story.append(Spacer(1, 12))
    
    doc.build(story)

def main():
    directory_structure = get_chronos_directory_structure('codebase_directories_and_files')
    local_codebase_directory = directory_structure['local_codebase_directory']
    output_pdf = directory_structure['output_pdf']

    get_latest_codebase_content(local_codebase_directory)
    file_list = extract_filenames_from_codebase_list(local_codebase_directory)
    convert_code_to_pdf(file_list, output_pdf, local_codebase_directory)

if __name__ == "__main__":
    main()


