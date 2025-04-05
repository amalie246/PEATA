import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableView, QMessageBox)
from PyQt5.QtCore import QAbstractTableModel, Qt

# Custom model to show DataFrame
class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame()):
        super().__init__()
        self._df = df 

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._df.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return str(self._df.columns[section])
        else:
            return str(self._df.index[section])


class DataViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("PEATA Data Viewer")
        self.setGeometry(100,100,800,600)

        self.table_view = QTableView()
        self.open_button = QPushButton("Open CSV/Excel")

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        self.open_button.clicked.connect(self.load_file)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV or Excel file",
            "",
            "CSV files (*.csv);;Excel files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")

            self.table_view.setModel(PandasModel(df))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")

# For testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataViewer()
    window.show()
    sys.exit(app.exec_())
        