import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

from compression.algorithm_factory import AlgorithmFactory
from encryption.encryption_manager import EncryptionManager
from encryption.password import Password
from history.task_history import TaskHistory, generate_task_id
from history.compression_task import CompressionTask

logger = logging.getLogger(__name__)


class Compressor(ABC):
    def __init__(self):
        self.task_history = TaskHistory()

    @abstractmethod
    def run(self):
        pass

    def compress(
            self,
            files: list[str],
            algorithm: str,
            destination: str,
            password: Password = None,
    ):
        try:
            algorithm = AlgorithmFactory.get_algorithm(algorithm)
            compressed_file_path = algorithm.compress(files, destination)
            if password:
                em = EncryptionManager()
                with open(compressed_file_path, "rb") as compressed_file:
                    compressed_data = compressed_file.read()

                data = em.encrypt(compressed_data, password)
                compressed_encrypted_file_path = compressed_file_path + ".enc"

                with open(
                        compressed_encrypted_file_path, "wb"
                ) as compressed_encrypted_file:
                    compressed_encrypted_file.write(data)
                os.remove(compressed_file_path)

            self._log_compression_task(files, algorithm, "Completed", "compress")
        except Exception as e:
            self._log_compression_task(
                files, algorithm, f"Failed: {str(e)}", "compress"
            )
            logger.error(f"Error during compression: {e}")
            raise e

    def decompress(self, archive: str, destination: str, password: Password = None):
        algorithm = None
        original_path = archive
        try:
            if password and archive.endswith(".enc"):
                em = EncryptionManager()
                with open(archive, "rb") as compressed_encrypted_file:
                    compressed_encrypted_data = compressed_encrypted_file.read()
                compressed_data = em.decrypt(compressed_encrypted_data, password)
                compressed_file_path = archive.replace(".enc", "")
                with open(compressed_file_path, "wb") as compressed_file:
                    compressed_file.write(compressed_data)
            else:
                compressed_file_path = archive

            algorithm = AlgorithmFactory.detect_algorithm_by_filepath(compressed_file_path)
            algorithm.decompress(compressed_file_path, destination)

            if compressed_file_path != original_path:
                os.remove(compressed_file_path)

            self._log_compression_task([archive], algorithm, "Completed", "decompress")
        except Exception as e:
            if compressed_file_path != original_path:
                os.remove(compressed_file_path)

            self._log_compression_task(
                [archive], algorithm, f"Failed: {str(e)}", "decompress"
            )
            logger.error(f"Error: {e}")
            raise e

    def _log_compression_task(self, files, algorithm, status, direction):
        task = CompressionTask(
            task_id=generate_task_id(),
            files=files,
            algorithm=algorithm,
            date=datetime.now(),
            status=status,
            direction=direction,
        )
        self.task_history.add_entry(task)
        logger.info(f"Compression task logged: {task.to_dict()}")
