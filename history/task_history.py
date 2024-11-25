import json
import os

from datetime import datetime

from history.compression_task import CompressionTask


class TaskHistory:
    HISTORY_FILE = "../task_history.json"

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


def generate_task_id():
    return int(datetime.now().timestamp())
