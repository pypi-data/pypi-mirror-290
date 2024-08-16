"""
This module implements part of the Python DBAPI 2.0 as described in https://www.python.org/dev/peps/pep-0249/ .
"""

import datetime
import decimal
import json
import logging
from collections import namedtuple
from typing import Any, Dict, List, Optional, Tuple

from clapdb import exceptions
from clapdb.client import GET_META_OPERATION, Client

from clapdb.exceptions import (  # noqa:F401 isort:skip
    DatabaseError,
    Error,
    InterfaceError,
    InternalError,
    NotSupportedError,
    Warning,
)

apilevel = "2.0"
threadsafety = 1  # Threads may share the module, but not connections.
paramstyle = "qmark"


logger = logging.getLogger(__name__)


CursorDescriptionRow = namedtuple(
    "CursorDescriptionRow",
    ["name", "type", "display_size", "internal_size", "precision", "scale", "null_ok"],
)

CursorDescriptionType = List[CursorDescriptionRow]


_converter_map = {
    "bool": bool,
    "int2": int,
    "int4": int,
    "bigint": int,
    "uint16": int,
    "uint32": int,
    "uint64": int,
    "float4": float,
    "float8": float,
    "numeric": decimal.Decimal,
    "time": datetime.time.fromisoformat,
    "date": datetime.date.fromisoformat,
    "timestamp": datetime.datetime.fromisoformat,
    "timestamptz": datetime.datetime.fromisoformat,
    "enum": str,
    "text": str,
    "ipv4": str,
    # The calculation rule of Postgres interval is special. Converting it to Python timedelta may result in information loss.
    "interval": str,
}


def _convert_result(data, description):
    result = []
    for i in range(len(data)):
        result.append([])

    for row_index, row in enumerate(data):
        for col_index, desc in enumerate(description):
            converter = _converter_map.get(desc[1], str)
            result[row_index].append(converter(row[col_index]))
    return result


class Cursor(object):
    def __init__(self, client: Client):
        self.client = client

        self.description: CursorDescriptionType = []
        self._result = None
        self._offset = 0

    def close(self):
        pass

    def _get_meta(self):
        # get json text of meta
        text = self.client.get_meta()

        # result of get_meta has one row and one column with string type
        self.description = [("meta", "string", None, None, None, None, None)]

        # first list for rows, second list for columns
        self._result = [[text]]
        self._offset = 0
        self.rowcount = None

    def execute(self, operation, parameters: Optional[Dict[str, Any]] = None):
        if operation == GET_META_OPERATION:
            return self._get_meta()

        text = self.client.execute(operation)

        try:
            resp_json = json.loads(text)
            columns = resp_json["headers"]
            types = resp_json["types"]
            desc = []
            for index, column in enumerate(columns):
                type_ = types[index]
                desc.append((column, type_, None, None, None, None, None))

            self._result = _convert_result(resp_json["data"], desc)
            self.description = desc
            self._offset = 0
            self.rowcount = len(self._result)
        except Exception as ex:
            raise exceptions.InternalError("invalid query result") from ex

    def fetchall(self) -> List[Tuple[Any, ...]]:
        if not self._result:
            return []

        if self._offset >= len(self._result):
            return []

        old_offset = self._offset
        self._offset = len(self._result)
        return self._result[old_offset:]

    def fetchone(self) -> Tuple[Any, ...]:
        if not self._result:
            return None

        if self._offset >= len(self._result):
            return None

        old_offset = self._offset
        self._offset += 1
        return self._result[old_offset]

    def fetchmany(self, size=None) -> List[Tuple[Any, ...]]:
        if not self._result:
            return []

        if self._offset >= len(self._result):
            return []

        old_offset = self._offset
        if not size:
            self._offset = len(self._result)
            return self._result[old_offset:]

        self._offset += size
        return self._result[old_offset : old_offset + size]


class Connection(object):
    def __init__(self, client: Client):
        self.client = client

    def cursor(self) -> Cursor:
        return Cursor(self.client)

    def close(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


def connect(
    scheme: str,
    netloc: str,
    username: str,
    password: str,
    database: str,
    timeout: float,
) -> Connection:
    """
    Constructor for creating a connection to the database.

    See :py:class:`Client` for arguments.

    :returns: a :py:class:`Connection` object
    """
    client = Client(scheme, netloc, username, password, database, timeout)
    return Connection(client)
