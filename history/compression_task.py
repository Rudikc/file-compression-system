from datetime import datetime


class CompressionTask:
    def __init__(self, task_id, files, algorithm, date, status, direction):
        self.task_id = task_id
        self.files = files
        self.algorithm = algorithm.__class__.__name__
        self.date = date
        self.status = status
        self.direction = direction

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "files": self.files,
            "algorithm": self.algorithm,
            "date": self.date.isoformat(),
            "status": self.status,
            "direction": self.direction,
        }

    @staticmethod
    def from_dict(data):
        return CompressionTask(
            task_id=data["task_id"],
            files=data["files"],
            algorithm=data["algorithm"],
            date=datetime.fromisoformat(data["date"]),
            status=data["status"],
            direction=data["direction"],
        )
