"""
File Name: convert_wiki_to_pdf.py

Purpose:  This script converts the GitHub Wiki for Beau's AI Scheduling Assistant, Chronos.
          * Generates a Table of Contents file ('toc.md') based on the '_Sidebar.md' file in a specified wiki directory.
          * Converts a collection of Markdown files from the wiki directory into a PDF document using Pandoc.
          * Saves the generated PDF directly to Google Drive.

Author: Beau Magnum

Date: 2024-04-03

Usage:
      python wiki_to_pdf.py
"""


import os # Allows python to use os commands, similar to the way commands are executed in the terminal
import subprocess # Allows python to run other programs within the script, in this case "pandoc", the document conversion software

# --- Configuration ---
wiki_dir = "/Users/kennmagnum/Chronos-HoM.wiki/"  # Location of the repo on my harddrive
table_of_contents_file = "script-util_Table-of-Content.md" # Auto-generated table of contents based on the wiki's '_Sidebar' file
output_pdf = "Chronos-HoM-Wiki.pdf"
googleDrive = "/Users/kennmagnum/Library/CloudStorage/GoogleDrive-kenn.magnum@gmail.com/My Drive/" # "/Users/kennmagnum/Library/CloudStorage/GoogleDrive-kenn.magnum@gmail.com/My Drive"

# --- Git pull for updating wiki on local computer ---
def update_wiki():
    os.chdir(wiki_dir) # Change directory to the wiki location
    subprocess.run(["git", "pull"])

            
# --- Generate a PDF format using "Pandoc" ---
def generate_pdf(file_list):
#    wiki_dir = os.path.dirname(os.path.join(googleDrive, output_pdf))
#    os.makedirs(wiki_dir, exist_ok=True)

    with open(os.path.join(wiki_dir, table_of_contents_file), 'r') as toc_file:
        toc_lines = toc_file.readlines()

    ordered_markdown_files = []
    for line in toc_lines:
        if line.startswith('#'):  # Assuming headings signify filenames
            filename = line.strip().split(' ')[1]  # Extract 'HOME.md'
            ordered_markdown_files.append(filename)

    pandoc_command = [
    "pandoc",
    "-o", os.path.join(googleDrive, output_pdf),
    "--toc",
    "--toc-depth=2", # Include headings up to level 2
    table_of_contents_file
    ]
    pandoc_command.extend(ordered_markdown_files) # Add all the Markdown files from our ordered list
    subprocess.run(pandoc_command, cwd=wiki_dir)
    
# --- Main Execution ---
if __name__ == "__main__":
    update_wiki()
    file_list = generate_toc() # Stores the returned file_list
    generate_pdf(file_list)