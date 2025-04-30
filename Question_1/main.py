#!/usr/bin/env python3
"""
Minimal Main Module
"""

import sys
from data_access import load_data, get_scientist_id, get_scientist_name, search_scientists
from scientists_network import shortest_path, print_path


def main():
    # Check arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <data_directory>")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    
    # Load data
    print(f"Loading data from '{data_dir}'...")
    success, message = load_data(data_dir)
    if not success:
        print(f"Error: {message}")
        sys.exit(1)
    
    print("Data loaded successfully.")
    
    while True:
        # Get source scientist
        source_input = input("\nSource scientist name (or 'quit' to exit): ").strip()
        if source_input.lower() == 'quit':
            break
        
        # Search scientists
        matches = search_scientists(source_input)
        if not matches:
            print(f"No scientists found matching '{source_input}'.")
            continue
        
        if len(matches) > 1:
            print(f"Multiple matches for '{source_input}':")
            for i, (sci_id, name) in enumerate(matches, 1):
                print(f"  {i}. {name}")
            
            choice = input("Select number (or 0 to try again): ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    continue
                if choice_num < 1 or choice_num > len(matches):
                    print("Invalid choice.")
                    continue
                source_id = matches[choice_num-1][0]
                source_name = matches[choice_num-1][1]
            except ValueError:
                print("Please enter a valid number.")
                continue
        else:
            source_id = matches[0][0]
            source_name = matches[0][1]
            print(f"Using scientist: {source_name}")
        
        # Get target scientist
        target_input = input("Target scientist name (or 'quit' to exit): ").strip()
        if target_input.lower() == 'quit':
            break
        
        # Search scientists
        matches = search_scientists(target_input)
        if not matches:
            print(f"No scientists found matching '{target_input}'.")
            continue
        
        if len(matches) > 1:
            print(f"Multiple matches for '{target_input}':")
            for i, (sci_id, name) in enumerate(matches, 1):
                print(f"  {i}. {name}")
            
            choice = input("Select number (or 0 to try again): ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    continue
                if choice_num < 1 or choice_num > len(matches):
                    print("Invalid choice.")
                    continue
                target_id = matches[choice_num-1][0]
                target_name = matches[choice_num-1][1]
            except ValueError:
                print("Please enter a valid number.")
                continue
        else:
            target_id = matches[0][0]
            target_name = matches[0][1]
            print(f"Using scientist: {target_name}")
        
        # Find path
        print(f"Searching for connection...")
        path = shortest_path(source_id, target_id)
        
        # Display results
        if source_id == target_id:
            print(f"Same scientist: '{source_name}'.")
        elif path is None:
            print(f"No connection found between '{source_name}' and '{target_name}'.")
        else:
            degrees = len(path) - 1
            print(f"{degrees} degree{'s' if degrees > 1 else ''} of separation.")
            print_path(path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")