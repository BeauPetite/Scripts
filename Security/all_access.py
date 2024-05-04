"""
File Name: all_access.py

Purpose: This Python script provides access to secure information and system detail from 1Password.

**Functionality:**

* Retrieves the user's home directory.
* Retrieves the system username.
* Retrieves the directory structure from 1Password.

**Benefits:**

* Centralizes access to secure information.
* Provides a consistent way to access system details.

**Instructions:**

1. Import the `all_access.py` script into your Python file.
2. Call the `get_user_directory()` function to retrieve the user's home directory.
3. Call the `get_system_username()` function to retrieve the system username.
4. Call the `get_chronos_directory_structure()` function to retrieve the directory structure from 1Password.

**Usage:**

import all_access

user_home = all_access.get_user_directory()
system_username = all_access.get_system_username()
directory_structure = all_access.get_chronos_directory_structure()

Author: Beau Magnum

Date: 2024-04-03

"""
import json
import os
import subprocess

def get_user_directory():
    return os.path.expanduser("~") 

def get_system_username():
    home_directory = get_user_directory()
    return os.path.basename(home_directory)

def get_chronos_directory_structure():
    try:
        # Retrieve the secure note from 1Password
        output = subprocess.check_output(
            ["op", "item", "get", "chronos_script_data", "--format=json"],
            text=True
        )
        
        data = json.loads(output) # Load the JSON data from 1Password's secure note

        # Parse the details from the 1Password's secure note. If ADDING ADDITIONAL FIELDS to chronos_script_data, this is the code that needs to be reproduced 
        for field in data.get('fields', []):
            if field.get('label') == 'directories_and_files': # 'label' is the named used by 1Password Beau set the label to 'directories_and_files'
                details = json.loads(field['value'])
                break
        else:
            raise ValueError("Directory and file names not found in 1Password's secure note.")
        
        # Replace the placeholder with the actual user's home directory.
        user_home = get_user_directory()
        for key, value in details.items():
            details[key] = value.replace('{home_directory}', user_home.strip('/'))
        
        return details
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving directory structure from 1Password: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
    except ValueError as e:
        print(e)

# Ensure this function is being called properly for testing
if __name__ == "__main__":
    directory_structure = get_chronos_directory_structure()
    print(directory_structure)
