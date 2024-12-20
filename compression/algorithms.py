import gzip
import lzma
import os
import tarfile
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
        tar_path = destination + ".tar"
        gz_path = destination + ".tar.gz"

        with tarfile.open(tar_path, "w") as tar:
            for file in files:
                tar.add(file, arcname=os.path.basename(file))

        with open(tar_path, "rb") as f_in:
            with gzip.open(gz_path, "wb") as f_out:
                f_out.writelines(f_in)

        os.remove(tar_path)
        return gz_path

    def decompress(self, archive: str, destination: str):
        tar_path = archive.replace(".gz", "")

        with gzip.open(archive, "rb") as f_in:
            with open(tar_path, "wb") as f_out:
                f_out.write(f_in.read())

        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(destination)

        os.remove(tar_path)


class LzmaAlgorithm(Algorithm):
    def compress(self, files: list[str], destination: str):
        tar_path = destination + ".tar"
        xz_path = destination + ".tar.xz"

        with tarfile.open(tar_path, "w") as tar:
            for file in files:
                tar.add(file, arcname=os.path.basename(file))

        with open(tar_path, "rb") as f_in:
            with lzma.open(xz_path, "wb") as f_out:
                f_out.writelines(f_in)

        os.remove(tar_path)
        return xz_path

    def decompress(self, archive: str, destination: str):
        tar_path = archive.replace(".xz", "")

        with lzma.open(archive, "rb") as f_in:
            with open(tar_path, "wb") as f_out:
                f_out.write(f_in.read())

        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(destination)

        os.remove(tar_path)


class UnsupportedAlgorithmException(Exception):
    def __init__(self, message="Unsupported algorithm specified"):
        self.message = message
        super().__init__(self.message)
