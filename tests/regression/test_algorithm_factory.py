import pytest

from compression.algorithm_factory import AlgorithmFactory
from compression.algorithms import (
    ZipAlgorithm,
    GzipAlgorithm,
    LzmaAlgorithm,
    UnsupportedAlgorithmException,
)


def test_get_algorithm_zip():
    algorithm = AlgorithmFactory.get_algorithm("zip")
    assert isinstance(algorithm, ZipAlgorithm)


def test_get_algorithm_gzip():
    algorithm = AlgorithmFactory.get_algorithm("gzip")
    assert isinstance(algorithm, GzipAlgorithm)


def test_get_algorithm_lzma():
    algorithm = AlgorithmFactory.get_algorithm("lzma")
    assert isinstance(algorithm, LzmaAlgorithm)


def test_get_algorithm_invalid():
    with pytest.raises(
        UnsupportedAlgorithmException, match="Unsupported algorithm: invalid"
    ):
        AlgorithmFactory.get_algorithm("invalid")


def test_detect_algorithm_by_filepath_zip():
    algorithm = AlgorithmFactory.detect_algorithm_by_filepath("test_archive.zip")
    assert isinstance(algorithm, ZipAlgorithm)


def test_detect_algorithm_by_filepath_gzip():
    algorithm = AlgorithmFactory.detect_algorithm_by_filepath("test_archive.tar.gz")
    assert isinstance(algorithm, GzipAlgorithm)


def test_detect_algorithm_by_filepath_lzma():
    algorithm = AlgorithmFactory.detect_algorithm_by_filepath("test_archive.tar.xz")
    assert isinstance(algorithm, LzmaAlgorithm)


def test_detect_algorithm_by_filepath_invalid_extension():
    with pytest.raises(
        UnsupportedAlgorithmException, match="Unsupported file extension: .unknown"
    ):
        AlgorithmFactory.detect_algorithm_by_filepath("test_archive.unknown")


def test_detect_algorithm_by_filepath_no_extension():
    with pytest.raises(
        UnsupportedAlgorithmException, match="Unsupported file extension: "
    ):
        AlgorithmFactory.detect_algorithm_by_filepath("test_archive")
