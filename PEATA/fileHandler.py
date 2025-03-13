from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from PEATA.config import CSV_FOLDER, EXPORTS_FOLDER


class FileHandler:
    
    def __init__(self):
        self.data = None # Store the DataFrame
        self.file_path = self.get_latest_csv_file() 
        
    # No need to manually specify the filename each time
    def get_latest_csv_file(self):
        # Find the most recently modified CSV file in the CSV folder
        csv_files = list(Path(CSV_FOLDER).glob("*.csv"))
        if not csv_files:
            print("No CSV files found.")
            return None
        
        latest_file = max(csv_files, key=os.path.getmtime) # Get the most recent file
        print(f"Latest CSV file detected: {latest_file}")
        return latest_file
    
    def open_file(self):
        # Opens the latest CSV file and returns the data as a pandas DataFrame.
        if not self.file_path:
            print("No CSV file to open.")
            return None
        try:
            self.data = pd.read_csv(self.file_path)         
            print(f"File {self.file_path} opened successfully.")
            return self.data
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except Exception as e:
            print(f"Error opening file {self.file_path}: {e}")
        
        
    def close_file(self):
       # Closes the file by deleting the stored DataFrame reference.
        if self.data is not None:
            self.data = None # Clear the DataFrame from memory
            print("File data has been cleared from memory.")
        else: 
            print("No file data to close.")
            

    def export_as_pdf(self):
        if self.data is None:
            print("No data available to export.")
            return
        try:
            output_pdf = Path(EXPORTS_FOLDER) / (self.file_path.stem + ".pdf") # Same name as CSV
            c = canvas.Canvas(str(output_pdf),pagesize=letter)
            width, height = letter
            
            c.drawString(30, height - 30, "Exported Data") 
            
            # Starting position for table
            x_offset = 30
            y_offset = height - 50
            line_height = 15
            
            # Column headers
            columns = list(self.data.columns)
            c.drawString(x_offset, y_offset, " | ".join(columns))
            y_offset -= line_height 
            
            # rows (limit to avoid page overflow)
            max_row_per_page = 40
            row_count = 0
            
            for index, row in self.data.iterrows():
                row_data = " | ".join(str(row[col]) for col in columns)
                c.drawString(x_offset, y_offset, row_data)
                y_offset -= line_height
                row_count += 1
                
                if row_count >= max_row_per_page:
                    c.showPage()
                    y_offset = height - 50
                    row_count = 0
            
            c.save()
            print(f"PDF exported successfully: {output_pdf}")
             
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            
    def export_as_excel(self):
        if self.data is None:
            print("No data available to export.")
            return
        try:
            output_excel = Path(EXPORTS_FOLDER) / (self.file_path.stem + ".xlsx") # Same name as CSV
            with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
                self.data.to_excel(writer, sheet_name="Sheet1", index=False)
                
            print(f"Excel file exported successfully: {output_excel}")
            
        except Exception as e:
            print(f"Error exproting to Excel: {e}")
            
            
# """ Example Usage """            
# file_handler = FileHandler()  # Instantiate the class
# data = file_handler.open_file()

# if data is not None: 

# """ Export as PDF and Excel"""
# file_handler.export_as_pdf()
# file_handler.export_as_excel()


# """ Close file """
# file_handler.close_file()
