"""
Utils Module - Helper functions for the scientists connection application
"""

import os
import sys


def validate_data_files(data_dir):
    """
    Validate that all required data files exist in the specified directory
    
    Args:
        data_dir (str): Path to data directory
    
    Returns:
        tuple: (success, message) where success is a boolean and message is a string
    """
    required_files = ['scientists.csv', 'collaborations.csv']
    
    if not os.path.isdir(data_dir):
        return False, f"Directory '{data_dir}' does not exist"
    
    missing_files = []
    for filename in required_files:
        filepath = os.path.join(data_dir, filename)
        if not os.path.isfile(filepath):
            missing_files.append(filename)
    
    if missing_files:
        return False, f"Missing required file(s): {', '.join(missing_files)}"
    
    return True, "All required files present"


def print_usage():
    """Print usage instructions for the program"""
    print("Scientists Connection Finder")
    print("---------------------------")
    print("Find degrees of separation between scientists based on collaboration data.")
    print("\nUsage:")
    print("  python main.py <data_directory>")
    print("\nWhere:")
    print("  <data_directory> is the path to the directory containing:")
    print("    - scientists.csv: Contains scientist information")
    print("    - collaborations.csv: Contains collaboration information")


def get_input_with_default(prompt, default=None):
    """
    Get user input with a default value
    
    Args:
        prompt (str): Prompt to display to the user
        default (str, optional): Default value if user enters nothing
    
    Returns:
        str: User input or default value
    """
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()