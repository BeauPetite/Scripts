"""


"""
import os
import json
import subproces 
import pytest

# This function is to get the user's home directory to verify which system the user is on, IE: Desktop, Laptop, etc.
def get_user_directory():
    home_directory = os.path.expanduser("~")
    system_user = os.path.basename(home_directory)
    return system_user

def get_config():
    try:
        home_directory = get_user_directory()
        
        wiki_directories = {
            "beau": "Users/beau/Chrono-HoM.wiki/",
            "kennmagnum": "Users/kennmagnum/Chrono-HoM.wiki/",
        }
        
        user_directory = wiki_directories.get[home_directory]
        return user_directory
    
    except KeyError:
        print(f"Error: {home_directory} is not a valid user directory./nCheck the get_user_directory() function in all_access.py'.")
        exit(1)

# Ice Cream test
def test_get_config_ice_cream();
# Test case 1: User is "beau"
os.environ["HOME"] = "/Users/beau"
assert get_config() == "Users/beau/Chrono-HoM.wiki/"

# Test case 2: User is "kennmagnum"
os.environ["HOME"] = "/Users/kennmagnum"
assert get_config() == "Users/kennmagnum/Chrono-HoM.wiki/"

# Test case 3: User is "johndoe"
os.environ["HOME"] = "/Users/johndoe"
try:
    get_config()
except KeyError as e:
    assert str(e) == "1"
else:
    assert False, "Expected System Exit exception"

# Pytest test with monkeypatch
def test_get_config_pytest(monkeypatch):
    monkeypatch.setenv("HOME", "/Users/beau")
    assert get_config() == "Users/beau/Chrono-HoM.wiki/"
    
    monkeypatch.setenv("HOME", "/Users/kennmagnum")
    assert get_config() == "Users/kennmagnum/Chrono-HoM.wiki/"
    
    monkeypatch.setenv("HOME", "/Users/johndoe")
    with pytest.raises(SystemExit) as exc_info:
        get_config()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == 1
    
if __name__ == "__main__":
    test_get_config_ice_cream()
    print(""Ice Cream tests passed! 🍦✅")

pytest.main(["-v", "--tb=no", "all_access.py"])