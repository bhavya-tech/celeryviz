import json


class Recorder:
    records = []

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def record(self, data: dict) -> None:
        with open(self.file_name, 'a') as f:
            f.write(json.dumps(data) + '\n')
