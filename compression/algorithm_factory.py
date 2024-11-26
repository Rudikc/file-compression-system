import os

from compression.algorithms import (
    ZipAlgorithm,
    GzipAlgorithm,
    LzmaAlgorithm,
    UnsupportedAlgorithmException,
)


class AlgorithmFactory:
    _ALGORITHMS = {
        "zip": ZipAlgorithm,
        "gzip": GzipAlgorithm,
        "lzma": LzmaAlgorithm,
    }

    @staticmethod
    def get_algorithm(name: str):
        if name in AlgorithmFactory._ALGORITHMS:
            return AlgorithmFactory._ALGORITHMS[name]()
        raise UnsupportedAlgorithmException(f"Unsupported algorithm: {name}")

    @staticmethod
    def detect_algorithm_by_filepath(filepath: str):
        extension_mapping = {
            ".zip": "zip",
            ".gz": "gzip",
            ".xz": "lzma",
        }
        ext = os.path.splitext(filepath)[1]
        if ext in extension_mapping:
            return AlgorithmFactory.get_algorithm(extension_mapping[ext])
        raise UnsupportedAlgorithmException(f"Unsupported file extension: {ext}")
