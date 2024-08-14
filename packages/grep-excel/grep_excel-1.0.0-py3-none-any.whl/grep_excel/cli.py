import argparse
import os
from .grep import ExcelGrep

def main():
    parser = argparse.ArgumentParser(description="Search Excel files for a pattern.")
    parser.add_argument('directory', nargs='?', default=os.getcwd(), help="Directory to search (defaults to current directory)")
    parser.add_argument('pattern', help="Pattern to search for")
    parser.add_argument('--exclude', '-v', help="Pattern to exclude")
    parser.add_argument('--print-row', action='store_true', help="Print entire row")
    
    args = parser.parse_args()
    
    # Create an instance of ExcelGrep and run the search
    grep = ExcelGrep(args.directory, args.pattern, exclude_pattern=args.exclude, print_row=args.print_row)
    grep.search_excel_files_in_dir()

if __name__ == "__main__":
    main()
