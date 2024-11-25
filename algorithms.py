import os
import zipfile
from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def compress(self, files, destination):
        pass

    @abstractmethod
    def decompress(self, archive, destination):
        pass


class ZipAlgorithm(Algorithm):
    def compress(self, files: list[str], destination: str):
        zip_path = destination + ".zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                zip_file.write(file, os.path.basename(file))
        return zip_path

    def decompress(self, archive: str, destination: str):
        with zipfile.ZipFile(archive, "r") as zip_file:
            zip_file.extractall(destination)


class GzipAlgorithm(Algorithm):
    def compress(self, files, destination):
        pass

    def decompress(self, archive, destination):
        pass


class LzmaAlgorithm(Algorithm):
    def compress(self, files, destination):
        pass

    def decompress(self, archive, destination):
        pass


_ALL_ALGORITHMS = {
    "zip": ZipAlgorithm(),
    "gzip": GzipAlgorithm(),
    "lzma": LzmaAlgorithm(),
}


def get_algorithm(algorithm: str) -> Algorithm:
    return _ALL_ALGORITHMS[algorithm]


def detect_algorithm_by_filepath(archive):
    extension = os.path.splitext(archive)[1]
    if extension == ".zip":
        return ZipAlgorithm()
    elif extension == ".gz":
        return GzipAlgorithm()
    elif extension == ".xz":
        return LzmaAlgorithm()
    else:
        raise ValueError("Unsupported archive format")
