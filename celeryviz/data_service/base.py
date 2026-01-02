from datetime import datetime
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

    url_endpoint_name: str = ""

    def __init__(self, *args, **kwargs):
        if not self.url_endpoint_name:
            raise NotImplementedError("Subclasses must define url_endpoint_name attribute.")

    async def fetch_events(self, *args, **kwargs) -> List[dict]:
        """Receive a list of event dictionaries from the data source."""
        raise NotImplementedError("Subclasses must implement fetch_events method.")
    
    async def head_method(self, *args, **kwargs):
        """Handle HEAD requests for event data."""
        raise NotImplementedError("Subclasses must implement head_method method.")


class AbstractConfigurableService:
    """Abstract service that can be configured via a config dictionary."""

    config_options: tuple = ()

    def __init__(self, config: dict):
        """Initialize the service with the provided configuration."""
        raise NotImplementedError("Subclasses must implement __init__ method.")