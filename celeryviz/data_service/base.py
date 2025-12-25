from typing import List


class AbstractEventSink:
    """Abstract service for dumping event data."""

    async def dump_events(self, events: List[dict]):
        """Dump a list of event dictionaries to the data store."""
        raise NotImplementedError("Subclasses must implement dump_events method.")


class AbstractEventRetriever:
    """
    Abstract service for querying event data.
    Not in use currently, will be used when we start sending stored events to clients.
    """

    async def fetch_events(self, *args, **kwargs) -> List[dict]:
        """Receive a list of event dictionaries from the data source."""
        raise NotImplementedError("Subclasses must implement fetch_events method.")