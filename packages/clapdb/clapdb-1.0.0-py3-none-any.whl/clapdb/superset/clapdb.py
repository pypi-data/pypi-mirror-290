from superset.db_engine_specs.base import BaseEngineSpec


class ClapDBEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method
    """Dialect for ClapDB"""

    engine = "clapdb"
    engine_name = "ClapDB"

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "date_trunc('second', {col})",
        "PT1M": "date_trunc('minute', {col})",
        "PT1H": "date_trunc('hour', {col})",
        "P1D": "date_trunc('day', {col})",
        "P1M": "date_trunc('month', {col})",
        "P1Y": "date_trunc('year', {col})",
    }
