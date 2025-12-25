import json
import logging
import aiofiles
from typing import List
from celeryviz.data_service.base import AbstractEventSink

logger = logging.getLogger(__name__)


class FileEventSink(AbstractEventSink):
    """File-based implementation of the AbstractEventSink."""

    def __init__(self, file_path: str):

        if file_path.endswith('.jsonl') or file_path.endswith('.ndjson'):
            self.file_path = file_path
            logger.info(f"Initialized event storage with file: {file_path}")
        else:
            raise ValueError("File extension must be .jsonl or .ndjson")

    async def dump_events(self, events: List[dict]):
        """Dump a list of event dictionaries to a file."""

        json_lines = [json.dumps(event) for event in events]
        write_data = "\n".join(json_lines) + "\n"

        async with aiofiles.open(self.file_path, "a") as f:
            await f.write(write_data)