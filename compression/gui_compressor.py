import sys
import json
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
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt5.QtCore import Qt

from compression.algorithms import (
    UnsupportedAlgorithmException,
    detect_algorithm_by_filepath,
)
from compression.compressor import Compressor
from settings.settings import Settings


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
        self.settings = Settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Compression System")
        self.resize(400, 200)  # Set the initial size of the window

        self.compress_button = QPushButton("Compress")
        self.compress_button.clicked.connect(self.compress_files)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress_archive)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)

        self.algorithm_label = QLabel("Algorithm:")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["zip", "gzip", "lzma"])
        self.algorithm_combo.setCurrentText(self.settings.default_algorithm)

        self.encryption_checkbox = QCheckBox("Enable Encryption")
        self.encryption_checkbox.setChecked(self.settings.encryption_enabled)
        self.encryption_checkbox.stateChanged.connect(self.toggle_password_input)

        self.password_label = QLabel("Password (Optional):")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setVisible(self.encryption_checkbox.isChecked())
        self.password_input.setVisible(self.encryption_checkbox.isChecked())

        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(self.encryption_checkbox)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.compress_button)
        layout.addWidget(self.decompress_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_settings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def toggle_password_input(self, state):
        self.password_label.setVisible(state == Qt.Checked)
        self.password_input.setVisible(state == Qt.Checked)

    def compress_files(self):
        self.update_progress_bar(0)
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Compress")
        if not files:
            return
        destination, _ = QFileDialog.getSaveFileName(
            self, "Save Compressed File", self.settings.default_destination
        )
        if not destination:
            return
        algorithm = self.algorithm_combo.currentText()

        password = self.get_password()
        if self.encryption_checkbox.isChecked() and not password:
            QMessageBox.warning(
                self, "Warning", "Please enter a password for encryption and try again."
            )
            return

        try:
            self.compressor.compress(files, algorithm, destination, password)
        except Exception as e:
            QMessageBox.warning(self, "Failure", str(e))
            return

        QMessageBox.information(self, "Success", "Compression completed successfully.")
        self.update_progress_bar(100)

    def decompress_archive(self):
        self.update_progress_bar(0)
        archive, _ = QFileDialog.getOpenFileName(self, "Select Archive to Decompress")
        if not archive:
            return
        destination = QFileDialog.getExistingDirectory(
            self,
            "Select Destination Directory",
            self.settings.default_destination,
        )
        if not destination:
            return
        password = self.get_password()
        try:
            self.compressor.decompress(archive, destination, password)
        except Exception as e:
            QMessageBox.warning(self, "Failure", str(e))
            return

        QMessageBox.information(
            self, "Success", "Decompression completed successfully."
        )
        self.update_progress_bar(100)

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

    def open_settings(self):
        dialog = SettingsDialog()
        if dialog.exec_() == QDialog.Accepted:

            self.settings = dialog.get_settings()
            self.algorithm_combo.setCurrentText(
                self.settings.get("default_algorithm", "zip")
            )
            self.encryption_checkbox.setChecked(
                self.settings.get("encryption_enabled", False)
            )
            self.save_settings()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settings")
        self.resize(300, 150)

        self.layout = QFormLayout()

        self.default_destination_input = QLineEdit(self.settings.default_destination)
        self.default_destination_button = QPushButton("Browse")
        self.default_destination_button.clicked.connect(self.choose_directory)

        destination_layout = QVBoxLayout()
        destination_layout.addWidget(self.default_destination_input)
        destination_layout.addWidget(self.default_destination_button)
        self.layout.addRow("Default Destination:", destination_layout)

        self.default_algorithm_combo = QComboBox()
        self.default_algorithm_combo.addItems(["zip", "gzip", "lzma"])
        self.default_algorithm_combo.setCurrentText(self.settings.default_algorithm)
        self.layout.addRow("Default Algorithm:", self.default_algorithm_combo)

        self.encryption_enabled_checkbox = QCheckBox()
        self.encryption_enabled_checkbox.setChecked(self.settings.encryption_enabled)
        self.layout.addRow(
            "Enable Encryption by Default:", self.encryption_enabled_checkbox
        )

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Default Destination")
        if directory:
            self.default_destination_input.setText(directory)

    def get_settings(self):
        return {
            "default_destination": self.default_destination_input.text(),
            "default_algorithm": self.default_algorithm_combo.currentText(),
            "encryption_enabled": self.encryption_enabled_checkbox.isChecked(),
        }
