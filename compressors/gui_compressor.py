import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)
from PyQt5.QtCore import Qt

from compressors.compressor import Compressor


class GuiCompressor(Compressor):
    def run(self):
        app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.show()
        sys.exit(app.exec_())


class MainWindow(QMainWindow):
    def __init__(self, compressor):
        super().__init__()
        self.compressor = compressor
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Compression System")
        self.resize(400, 200)  # Set the initial size of the window

        # Remove 'self' as parent
        self.compress_button = QPushButton("Compress")
        self.compress_button.clicked.connect(self.compress_files)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress_archive)

        self.algorithm_label = QLabel("Algorithm:")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["zip", "gzip", "lzma"])

        self.encryption_checkbox = QCheckBox("Enable Encryption")
        self.encryption_checkbox.stateChanged.connect(self.toggle_password_input)

        self.password_label = QLabel("Password (Optional):")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setVisible(False)
        self.password_input.setVisible(False)

        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(self.encryption_checkbox)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.compress_button)
        layout.addWidget(self.decompress_button)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_password_input(self, state):
        if state == Qt.Checked:
            self.password_label.setVisible(True)
            self.password_input.setVisible(True)
        else:
            self.password_label.setVisible(False)
            self.password_input.setVisible(False)

    def compress_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Compress")
        if not files:
            return
        destination, _ = QFileDialog.getSaveFileName(self, "Save Compressed File")
        if not destination:
            return
        algorithm = self.algorithm_combo.currentText()

        password = self.get_password()
        if self.encryption_checkbox.isChecked() and not password:
            QMessageBox.warning(
                self, "Warning", "Please enter a password for encryption and try again."
            )
            return

        self.compressor.compress(files, algorithm, destination, password)
        QMessageBox.information(self, "Success", "Compression completed successfully.")

    def decompress_archive(self):
        archive, _ = QFileDialog.getOpenFileName(self, "Select Archive to Decompress")
        if not archive:
            return
        destination = QFileDialog.getExistingDirectory(
            self, "Select Destination Directory"
        )
        if not destination:
            return
        password = self.get_password()
        self.compressor.decompress(archive, destination, password)
        QMessageBox.information(
            self, "Success", "Decompression completed successfully."
        )

    def get_password(self):
        if self.encryption_checkbox.isChecked():
            password = self.password_input.text()
            if not password:
                QMessageBox.warning(
                    self, "Warning", "Please enter a password for encryption."
                )
                return None
            return password
        else:
            return None
