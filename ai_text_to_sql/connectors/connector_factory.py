import sys
import inspect
from typing import Optional, Dict, Type

from ai_text_to_sql.connectors import *
from .connector import Connector


class ConnectorFactory:
    """
    The class for building database connectors.
    """
    @staticmethod
    def build_connector(name: str, connection_data: Optional[Dict]) -> Connector:
        """
        Build a database connector.
        :param name: The name of the connector.
        :param connection_data: A dictionary containing the configuration parameters for the database connection.
        :return: A database connector.
        """
        connectors = ConnectorFactory._discover_connectors()
        if name in connectors:
            return connectors[name](connection_data)
        else:
            raise ValueError(f"Unsupported connector: {name}")

    @staticmethod
    def _discover_connectors() -> Dict[str, Type[Connector]]:
        """
        Discover available connectors dynamically.
        :return: A dictionary mapping connector names to their corresponding classes.
        """
        connectors = {}
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and issubclass(obj, Connector) and obj is not Connector:
                connectors[obj.__name__[:-9]] = obj  # Remove "Connector" from class name
        return connectors
