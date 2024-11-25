import os
import shutil
import subprocess
import json
import pytest


@pytest.fixture(scope="function")
def setup_test_environment():
    test_dir = "test_files_cli"
    output_dir = "output_files_cli"
    sample_files = ["file1.txt", "file2.txt"]
    task_history_path = "../task_history.json"

    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    for file in sample_files:
        with open(os.path.join(test_dir, file), "w") as f:
            f.write(f"Content of {file}")

    yield test_dir, output_dir, sample_files, task_history_path

    shutil.rmtree(test_dir)
    shutil.rmtree(output_dir)


def test_cli_compress_decompress_no_encryption(setup_test_environment):
    test_dir, output_dir, sample_files, task_history_path = setup_test_environment
    compressed_file = os.path.join(output_dir, "test_archive")

    subprocess.run(
        [
            "python",
            "../main.py",
            "compress",
            "-a",
            "zip",
            "-f",
            *[os.path.join(test_dir, f) for f in sample_files],
            "-o",
            compressed_file,
        ],
        check=True,
    )

    compressed_file = compressed_file + ".zip"
    assert os.path.exists(compressed_file)

    subprocess.run(
        ["python", "../main.py", "decompress", "-f", compressed_file, "-o", output_dir],
        check=True,
    )

    for file in sample_files:
        decompressed_file = os.path.join(output_dir, file)
        assert os.path.exists(decompressed_file)
        with open(decompressed_file, "r") as f:
            assert f.read() == f"Content of {file}"

    # Verify task history
    assert os.path.exists(task_history_path)
    with open(task_history_path, "r") as f:
        history = json.load(f)
        assert history[-2]["status"] == "Completed"
        assert history[-2]["direction"] == "compress"
        assert history[-1]["status"] == "Completed"
        assert history[-1]["direction"] == "decompress"


def test_cli_compress_decompress_with_encryption(setup_test_environment):
    test_dir, output_dir, sample_files, task_history_path = setup_test_environment
    compressed_file = os.path.join(output_dir, "test_archive")
    password = "StrongPassword123"

    subprocess.run(
        [
            "python",
            "../main.py",
            "compress",
            "-a",
            "gzip",
            "-f",
            *[os.path.join(test_dir, f) for f in sample_files],
            "-o",
            compressed_file.replace(".enc", ""),
            "-p",
            password,
        ],
        check=True,
    )

    compressed_file = compressed_file + ".tar.gz.enc"
    assert os.path.exists(compressed_file)

    subprocess.run(
        [
            "python",
            "../main.py",
            "decompress",
            "-f",
            compressed_file,
            "-o",
            output_dir,
            "-p",
            password,
        ],
        check=True,
    )

    for file in sample_files:
        decompressed_file = os.path.join(output_dir, file)
        assert os.path.exists(decompressed_file)
        with open(decompressed_file, "r") as f:
            assert f.read() == f"Content of {file}"

    assert os.path.exists(task_history_path)
    with open(task_history_path, "r") as f:
        history = json.load(f)
        assert history[-2]["status"] == "Completed"
        assert history[-2]["direction"] == "compress"
        assert history[-1]["status"] == "Completed"
        assert history[-1]["direction"] == "decompress"
