import csv
import sys

def process_csv_file(filename):
    """
    Process a single CSV file and print its contents.
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        list: List of rows from the CSV file (each row is a list of values)
    """
    print(f"\nProcessing file: {filename}")
    rows_data = []
    
    try:
        with open(filename, newline='', encoding='utf-8', errors='replace') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            
            # Print header row with formatting
            header = next(rows, None)
            if header:
                print("HEADER:", header)
                rows_data.append(header)
                
            # Print data rows
            row_count = 0
            for row in rows:
                print(f"Row {row_count}:", row)
                rows_data.append(row)
                row_count += 1
            
            print(f"Total rows processed: {row_count}")
            
        return rows_data
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error processing '{filename}': {e}")
        return []

def main():
    # List of CSV files to process
    csv_files = ["authors.csv", "papers.csv", "scientists.csv"]
    
    # If command line arguments are provided, use those instead
    if len(sys.argv) > 1:
        csv_files = sys.argv[1:]
    
    print(f"Will process {len(csv_files)} CSV files.")
    
    # Process each file
    for filename in csv_files:
        process_csv_file(filename)

if __name__ == "__main__":
    main()