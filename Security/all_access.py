"""


"""
import os
import json
import subprocess 

def get_user_directory():
    return os.path.expanduser("~") 

def get_system_username():
    home_directory = get_user_directory()
    return os.path.basename(home_directory)

def get_chronos_directory_structure():
    try:
        # REtrieve the secure note from 1Password
        output = subprocess.check_output(
            ["op", "item", "get", "chronos_directory_structure", "--format=json"],
            text=True
        )
        data = json.loads(output)
        # Parses the details from 1Password's Secure Note.
        details = json.loads(data['details']['notesPlain'])
        
        # Replace the placeholder with the actual user's home directory.
        user_home = get_user_directory()
        for key, value in details.items():
            details[key] = value.replace('{home_directory}', user_home.strip('/'))
            
        return details
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving directory structure from 1Password: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data from 1Password directory structure output")
        

# Example usage
if __name__ == "__main__":
    directory_structure = get_chronos_directory_structure()
    print(directory_structure)