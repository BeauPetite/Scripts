"""
File Name: convert_wiki_to_pdf.py

Purpose: This Python script automates the process of generating a PDF document from your 
GitHub Wiki repository. 

**Functionality:**

* Fetches the latest content from your specified GitHub Wiki repository.
* Extracts filenames and orders them based on the structure defined in your 
  `_Sidebar.md` file.
* Utilizes Pandoc to convert your Markdown files into a single, well-structured PDF.
* Uploads the generated PDF to your Google Drive (future functionality).

**Benefits:**

* Simplifies the process of creating and maintaining an up-to-date PDF version 
  of your Wiki documentation.
* Ensures consistency in formatting and presentation.

**Instructions:**

1. Configure the script with your GitHub repository details and Google Drive 
   credentials (to be implemented).
2. Run the script to generate and upload the PDF.

**Note:** This script is currently under development. 

Author: Beau Magnum

Date: 2024-04-03

Usage:
      python wiki_to_pdf.py
"""


import os # Allows python to use os commands, similar to the way commands are executed in the terminal
import re # Allows python to use regular expressions for pattern matching. In this case, we use it to extract filenames from the '_Sidebar.md' file
import subprocess # Allows python to run other programs within the script, in this case "pandoc", the document conversion software


# --- Configuration ---
local_wiki_directory = "/Users/kennmagnum/Chronos-HoM.wiki/"  # Location of the repo on my harddrive
output_pdf = "Chronos-HoM-Wiki.pdf"
googleDrive = "/Users/kennmagnum/Library/CloudStorage/GoogleDrive-kenn.magnum@gmail.com/My Drive/" # "/Users/kennmagnum/Library/CloudStorage/GoogleDrive-kenn.magnum@gmail.com/My Drive"

# --- Git pull for updating wiki on local computer ---
def get_latest_wiki_content():
    os.chdir(local_wiki_directory) # Change directory to the wiki location
    try:
        subprocess.run(["git", "pull"], check=True) # Run the git pull command to update the wiki on the local computer
    except subprocess.CalledProcessError as e:
        print(f"Error updating wiki: {e}") # Print an error message if the git pull command fails 

def extract_filenames_from_sidebar():
    file_list = []
    link_pattern = re.compile(r'\s*\[.*\]\((.*)\)')  # Extracts the filename from a Markdown link, in this case '[Display_Text](filename)'

    with open(os.path.join(local_wiki_directory, '_Sidebar.md'), 'r') as sidebar_file: # Open the '_Sidebar.md' file
        for line in sidebar_file: # Loop through each line in the file
            match = link_pattern.search(line) # Search for a link pattern in the line
            if match:
                filename = match.group(1) + '.md' # Extract the filename from the link and add the '.md'file extension to the end
                                # group(0) would be everything in the link_pattern, group(1) designates everything in the first set of parentheses.
                file_list.append(filename)
                
    return file_list # Return the list of filenames
            
# --- Generate a PDF format using "Pandoc" ---
def generate_pdf(file_list): # Using padoc to convert the markdown files to a PDF

    ordered_markdown_files = file_list # Ensure Correct Ordering of Files Based on '_Sidebar.md'  

    pandoc_command = [
# --- This function expects you to have a CSS file named 'pdf_formatting.css' 
# in the same directory as the wiki files ---

        "pandoc",
        "-o", os.path.join(googleDrive, output_pdf),  # Output file path
        "--toc", 
        "--toc-depth=4",  # Include headings up to level 4 in the ToC
        "--highlight-style=breezedark" # Use the 'breezedark' syntax highlighting style
        "--css=pdf_formatting.css" # File must be created seperately. Used for custom CSS styling
    ]

    pandoc_command.extend(ordered_markdown_files) # Add the ordered markdown files to the command
    subprocess.run(pandoc_command, cwd=local_wiki_directory)  # Run the pandoc command in the wiki directory

    
# --- Main Execution ---
if __name__ == "__main__":
    get_latest_wiki_content()
    file_list = extract_filenames_from_sidebar() # Stores the returned file_list
    generate_pdf(file_list)