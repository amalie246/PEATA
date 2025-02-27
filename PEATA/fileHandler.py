from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

file_path = Path(__file__).parent / "data" /"customers-100.csv"


class FileHandler:
    
    def __init__(self):
        self.data = None # Store the DataFrame
    
    def open_file(self, file_path):
        # Opens a CSV file and returns the data as a pandas DataFrame.
        try:
            self.data = pd.read_csv(file_path)         
            print(f"File {file_path} opened successfully.")
            return self.data
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")
        
        
    def close_file(self, file_path):
       # Closes the file by deleting the stored DataFrame reference.
        if self.data is not None:
            self.data = None # Clear the DataFrame from memory
            print("File data has been cleared from memory.")
        else: 
            print("No file data to close.")
            

    def export_as_pdf(self, output_file):
        if self.data is None:
            print("No data available to export.")
            return
        try:
            pdf_file = Path(output_file)
            c = canvas.Canvas(str(pdf_file),pagesize=letter)
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
            print(f"PDF exported successfully: {pdf_file}")
             
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            
    def export_as_excel(self, output_file):
        if self.data is None:
            print("No data available to export.")
            return
        try:
            excel_file = Path(output_file)
            with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
                self.data.to_excel(writer, sheet_name="Sheet1", index=False)
                
            print(f"Excel file exported successfully: {excel_file}")
            
        except Exception as e:
            print(f"Error exproting to Excel: {e}")
    
""" Open file """            
file_handler = FileHandler()  # Instantiate the class
data = file_handler.open_file(file_path)

""" Close file"""
# if data is not None: 
#     print(data.head()) # Display first few rows
    
# file_handler.close_file(file_path)

""" Export as PDF """
# output_pdf_path = Path(__file__).parent / "output" / "customers-100.pdf"
# file_handler.export_as_pdf(output_pdf_path)

""" Export as Excel """
output_excel_path = Path(__file__).parent / "output" / "customers-100.xlsx"
file_handler.export_as_excel(output_excel_path)
