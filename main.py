import sys
import ffmpeg
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QFileDialog, QComboBox, QMessageBox
)


class MediaConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media File Converter")
        self.setGeometry(300, 300, 400, 250)

        self.input_file = None
        self.output_directory = None

        # Create UI elements
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Label for instructions
        self.label = QLabel("Select a media file to convert:")
        layout.addWidget(self.label)

        # Button to select input file
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_btn)

        # Dropdown menu for output format
        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems(["mp3", "mp4", "m4a", "wav", "avi", "mov", "flac"])
        self.format_dropdown.setPlaceholderText("Select output format")
        layout.addWidget(self.format_dropdown)

        # Button to select output directory
        self.select_output_btn = QPushButton("Select Output Location")
        self.select_output_btn.clicked.connect(self.select_output_directory)
        layout.addWidget(self.select_output_btn)

        # Button to start conversion
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert_file)
        self.convert_btn.setEnabled(False)  # Disable until input file and output directory are selected
        layout.addWidget(self.convert_btn)

        # Set layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_file(self):
        """Opens a file dialog to select a media file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Media File", "", "All Files (*)")
        if file_name:
            self.input_file = file_name
            self.label.setText(f"Selected: {Path(file_name).name}")
            self.check_ready_to_convert()

    def select_output_directory(self):
        """Opens a dialog to select the output directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_directory = directory
            QMessageBox.information(self, "Output Directory Selected", f"Files will be saved to:\n{directory}")
            self.check_ready_to_convert()

    def check_ready_to_convert(self):
        """Enable the convert button if all necessary inputs are provided."""
        if self.input_file and self.output_directory:
            self.convert_btn.setEnabled(True)

    def convert_file(self):
        """Converts the selected media file to the specified format."""
        if not self.input_file:
            QMessageBox.warning(self, "Error", "No input file selected.")
            return

        if not self.output_directory:
            QMessageBox.warning(self, "Error", "No output directory selected.")
            return

        output_format = self.format_dropdown.currentText().strip().lower()
        if not output_format:
            QMessageBox.warning(self, "Error", "Please select an output format.")
            return

        input_path = Path(self.input_file)
        output_file = Path(self.output_directory) / f"{input_path.stem}.{output_format}"

        try:
            ffmpeg.input(str(input_path)).output(str(output_file)).run(overwrite_output=True)
            QMessageBox.information(self, "Success", f"File converted successfully!\nSaved as: {output_file}")
        except ffmpeg.Error as e:
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{e.stderr.decode('utf-8')}")

def main():
    app = QApplication(sys.argv)
    window = MediaConverterApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
