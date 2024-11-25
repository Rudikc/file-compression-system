import os
import shutil
import json
import pytest
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import Qt
from compression.gui_compressor import GuiCompressor
from settings.settings import Settings


@pytest.fixture(scope="function")
def setup_test_environment_gui():
    test_dir = "test_files_gui"
    output_dir = "output_files_gui"
    sample_files = ["file5.txt", "file6.txt"]
    task_history_path = "../task_history.json"

    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    for file in sample_files:
        with open(os.path.join(test_dir, file), "w") as f:
            f.write(f"Content of {file}")

    settings = Settings()
    settings.default_destination = output_dir
    settings.default_algorithm = "lzma"
    settings.encryption_enabled = True
    settings.save_settings()

    yield test_dir, output_dir, sample_files, task_history_path

    shutil.rmtree(test_dir)
    shutil.rmtree(output_dir)


def test_gui_compress_decompress_with_encryption_and_settings(
    setup_test_environment_gui, qtbot
):
    test_dir, output_dir, sample_files, task_history_path = setup_test_environment_gui
    app = QApplication.instance() or QApplication([])
    compressor = GuiCompressor()
    window = compressor.window

    window.algorithm_combo.setCurrentText("lzma")
    window.encryption_checkbox.setChecked(True)
    window.password_input.setText("StrongPassword123")

    def mock_getOpenFileNames(*args, **kwargs):
        return [os.path.join(test_dir, f) for f in sample_files], ""

    def mock_getSaveFileName(*args, **kwargs):
        return os.path.join(output_dir, "test_archive"), ""

    QFileDialog.getOpenFileNames = mock_getOpenFileNames
    QFileDialog.getSaveFileName = mock_getSaveFileName

    qtbot.mouseClick(window.compress_button, Qt.LeftButton)

    compressed_file = os.path.join(output_dir, "test_archive.tar.xz.enc")
    assert os.path.exists(compressed_file)

    def mock_getOpenFileName(*args, **kwargs):
        return compressed_file, ""

    def mock_getExistingDirectory(*args, **kwargs):
        return output_dir

    QFileDialog.getOpenFileName = mock_getOpenFileName
    QFileDialog.getExistingDirectory = mock_getExistingDirectory

    qtbot.mouseClick(window.decompress_button, Qt.LeftButton)

    for file in sample_files:
        decompressed_file = os.path.join(output_dir, file)
        assert os.path.exists(decompressed_file)
        with open(decompressed_file, "r") as f:
            assert f.read() == f"Content of {file}"

    assert window.algorithm_combo.currentText() == "lzma"
    assert window.encryption_checkbox.isChecked()
    assert window.password_input.text() == "StrongPassword123"

    assert os.path.exists(task_history_path)
    with open(task_history_path, "r") as f:
        history = json.load(f)
        assert history[-2]["status"] == "Completed"
        assert history[-2]["direction"] == "compress"
        assert history[-1]["status"] == "Completed"
        assert history[-1]["direction"] == "decompress"

    app.quit()
