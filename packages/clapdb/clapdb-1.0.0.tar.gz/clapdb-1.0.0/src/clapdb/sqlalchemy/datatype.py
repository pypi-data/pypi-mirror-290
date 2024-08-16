import logging

from sqlalchemy import types

logger = logging.getLogger(__name__)


type_map = {
    "bool": types.Boolean,
    "int2": types.Integer,
    "int4": types.Integer,
    "bigint": types.Integer,
    "uint16": types.Integer,
    "uint32": types.Integer,
    "uint64": types.BigInteger,
    "float4": types.Float,
    "float8": types.Float,
    "numeric": types.DECIMAL,
    "time": types.Time,
    "date": types.Date,
    "timestamp": types.DateTime,
    "timestamptz": types.DateTime,
    "enum": types.String,
    "text": types.Text,
    "ipv4": types.String,
    # The calculation rule of Postgres interval is special. Converting it to Python timedelta may result in information loss.
    "interval": types.String,
}


def get_type(data_type: str) -> int:
    type_ = type_map.get(data_type)
    if not type_:
        logger.warning(f"Unknown type found {data_type} reverting to string")
        type_ = types.String
    return type_
