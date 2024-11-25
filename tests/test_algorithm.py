import os
import shutil
import pytest

from compression.algorithms import (
    ZipAlgorithm,
    GzipAlgorithm,
    LzmaAlgorithm,
    detect_algorithm_by_filepath, UnsupportedAlgorithmException,
)


@pytest.fixture(scope="function")
def setup_test_environment():
    test_dir = "test_files"
    output_dir = "output_files"
    sample_files = ["file1.txt", "file2.txt"]

    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    for file in sample_files:
        with open(os.path.join(test_dir, file), "w") as f:
            f.write(f"Content of {file}")

    yield test_dir, output_dir, sample_files

    shutil.rmtree(test_dir)
    shutil.rmtree(output_dir)


@pytest.mark.parametrize(
    "algorithm_cls, extension",
    [
        (ZipAlgorithm, ".zip"),
        (GzipAlgorithm, ".tar.gz"),
        (LzmaAlgorithm, ".tar.xz"),
    ],
)
def test_compression_and_decompression(
    algorithm_cls, extension, setup_test_environment
):
    test_dir, output_dir, sample_files = setup_test_environment
    algorithm = algorithm_cls()
    compressed_file = os.path.join(output_dir, f"test_archive{extension}")

    archive = algorithm.compress(
        [os.path.join(test_dir, f) for f in sample_files],
        compressed_file.replace(extension, ""),
    )
    assert os.path.exists(archive)

    algorithm.decompress(archive, output_dir)
    for file in sample_files:
        decompressed_file = os.path.join(output_dir, file)
        assert os.path.exists(decompressed_file)
        with open(decompressed_file, "r") as f:
            assert f.read() == f"Content of {file}"


@pytest.mark.parametrize(
    "archive, expected_algorithm",
    [
        ("archive.zip", ZipAlgorithm),
        ("archive.tar.gz", GzipAlgorithm),
        ("archive.tar.xz", LzmaAlgorithm),
    ],
)
def test_detect_algorithm_by_filepath(archive, expected_algorithm):
    algorithm = detect_algorithm_by_filepath(archive)
    assert isinstance(algorithm, expected_algorithm)


@pytest.mark.parametrize(
    "path",
    [
        "",
        "archive.unknown",
        "archive.tar.bz2",
    ],
)
def test_detect_algorithm_by_filepath_invalid(path):
    with pytest.raises(UnsupportedAlgorithmException):
        detect_algorithm_by_filepath(path)
