import os
import pandas as pd
import time

class ExcelGrep:
    def __init__(self, directory, pattern, exclude_pattern=None, print_row=False):
        self.directory = directory
        self.pattern = pattern
        self.exclude_pattern = exclude_pattern
        self.print_row = print_row
        self.total_files = 0
        self.files_scanned = 0
        self.start_time = None

    def search_excel_file(self, file_path):
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

        total_cells = df.size
        cells_processed = 0

        for index, row in df.iterrows():
            for col in df.columns:
                value = str(row[col])
                cells_processed += 1
                if self.pattern in value:
                    if self.exclude_pattern and self.exclude_pattern in value:
                        continue
                    match_info = {
                        'file': file_path,
                        'row': index,
                        'column': col,
                        'value': value,
                        'row_data': row.to_dict() if self.print_row else None
                    }
                    self.print_match(match_info)

            # Print progress per file
            print(f"Scanning file {file_path}: {cells_processed}/{total_cells} cells processed ({(cells_processed / total_cells) * 100:.2f}%)")

    def print_match(self, match_info):
        file_info = f"File: {match_info['file']}, Row: {match_info['row']}, Column: {match_info['column']}"
        print(file_info)
        if match_info['row_data']:
            print(f"Row Data: {match_info['row_data']}")

    def search_excel_files_in_dir(self):
        self.start_time = time.time()

        # Calculate total files
        for root, _, files in os.walk(self.directory):
            self.total_files += len([file for file in files if file.endswith(('.xls', '.xlsx'))])
        
        # Scan each file
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(('.xls', '.xlsx')):
                    self.files_scanned += 1
                    file_path = os.path.join(root, file)
                    elapsed_time = time.time() - self.start_time
                    print(f"Scanning file {file_path} ({self.files_scanned}/{self.total_files})")
                    self.search_excel_file(file_path)

                    # Print overall progress with elapsed time
                    print(f"Overall progress: {self.files_scanned}/{self.total_files} files scanned ({(self.files_scanned / self.total_files) * 100:.2f}%)")
                    print(f"Total time elapsed: {elapsed_time:.2f} seconds\n")

        total_elapsed_time = time.time() - self.start_time
        print(f"Scan complete. Total time elapsed: {total_elapsed_time:.2f} seconds")
