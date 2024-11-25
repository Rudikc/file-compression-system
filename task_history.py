import json
import os

from datetime import datetime


class CompressionTask:
    def __init__(self, task_id, files, algorithm, date, status):
        self.task_id = task_id
        self.files = files
        self.algorithm = algorithm.__class__.__name__
        self.date = date
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "files": self.files,
            "algorithm": self.algorithm,
            "date": self.date.isoformat(),
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return CompressionTask(
            task_id=data["task_id"],
            files=data["files"],
            algorithm=data["algorithm"],
            date=datetime.fromisoformat(data["date"]),
            status=data["status"],
        )


class TaskHistory:
    HISTORY_FILE = "task_history.json"

    def __init__(self):
        self.tasks = []
        self._load_history()

    def add_entry(self, task):
        self.tasks.append(task)
        self.save_history()

    def get_recent_tasks(self):
        return self.tasks[-10:]

    def save_history(self):
        with open(self.HISTORY_FILE, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def _load_history(self):
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, "r") as f:
                tasks_data = json.load(f)
                self.tasks = [CompressionTask.from_dict(data) for data in tasks_data]
