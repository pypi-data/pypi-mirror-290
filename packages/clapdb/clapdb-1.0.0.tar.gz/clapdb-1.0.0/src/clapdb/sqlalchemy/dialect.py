import functools
import json
import urllib
from types import ModuleType
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from sqlalchemy.engine import default
from sqlalchemy.engine.url import URL

from clapdb import client, dbapi, exceptions
from clapdb.sqlalchemy.datatype import get_type

DEFAULT_TIMEOUT = 30.0


def handle_meta_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except exceptions.Error:
            raise
        except Exception as ex:
            raise exceptions.InternalError("invalid meta format") from ex

    return wrapper


def get_meta(connection):
    resp = connection.exec_driver_sql(client.GET_META_OPERATION)
    txt = resp.fetchall()[0][0]
    return json.loads(txt)


class HTTPDialect(default.DefaultDialect):
    name = "clapdb"
    driver = "http"
    scheme = "http"

    @classmethod
    def dbapi(cls) -> ModuleType:
        return dbapi

    def create_connect_args(self, url: URL) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        args: Sequence[Any] = list()
        kwargs: Dict[str, Any] = dict()

        netloc = url.host

        if url.port:
            netloc += ":" + str(url.port)

        if url.query.get("stage"):
            netloc += "/" + url.query["stage"]

        args.append(self.scheme)
        args.append(netloc)
        args.append(url.username)
        args.append(url.password)
        args.append(url.database)

        timeout = DEFAULT_TIMEOUT
        if "timeout" in url.query:
            try:
                timeout = float(url.query["timeout"])
            except ValueError:
                pass
        args.append(timeout)

        return (args, kwargs)

    @handle_meta_error
    def get_schema_names(self, connection, **kwargs):
        meta = get_meta(connection)
        return meta["schemas"].keys()

    @handle_meta_error
    def get_table_names(self, connection, schema=None, **kwargs) -> List[str]:
        meta = get_meta(connection)
        return meta["schemas"][schema]["tables"].keys()

    def get_view_names(self, connection, schema=None, **kwargs) -> List[str]:
        meta = get_meta(connection)
        return meta["schemas"][schema]["views"].keys()

    def get_pk_constraint(self, connection, table_name, schema=None, **kwargs):
        return []

    def get_foreign_keys(self, connection, table_name, schema=None, **kwargs):
        return []

    def get_indexes(self, connection, table_name, schema=None, **kwargs):
        return []

    @handle_meta_error
    def get_columns(self, connection, table_name, schema=None, **kw):
        meta = get_meta(connection)

        tables = meta["schemas"][schema].get("tables")
        views = meta["schemas"][schema].get("views")

        if tables and table_name in tables:
            columns = tables[table_name]["columns"]
        elif views and table_name in views:
            columns = views[table_name]["columns"]
        else:
            raise DatabaseError("table/view does not exist")

        result = []
        for column, props in columns.items():
            result.append(
                {
                    "name": column,
                    "type": get_type(props["type"]),
                    "nullable": props["nullable"],
                    "default": None,
                },
            )
        return result

    @handle_meta_error
    def has_table(self, connection, table_name, schema=None):
        meta = get_meta(connection)
        tables = meta["schemas"][schema]["tables"]
        return table_name in tables


class HTTPSDialect(HTTPDialect):
    driver = "https"
    scheme = "https"
