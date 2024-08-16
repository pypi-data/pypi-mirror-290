# clapdb-python-client

A basic database driver for connection ClapDB to Python, Superset
* SQLAlchemy 1.4 (limited feature set)
* Superset Connector

## Installation

`pip install clapdb`

clapdb client need Python 3.11 or higher

## Superset Connectivity

### for ClapDB instance

`clapdb+http://{user}.{tenant}:{password}@{host}:{port}/{database}?{timeout=30}`

> The timeout is a floating point number in seconds.

### for ClapDB lambda

`clapdb+https://{user}.{tenant}:{password}@{data_api_url_endpoint}/{database}?stage=production&{timeout=30}`

> The parameters can be found from ClapDB credentials [https://clapdb.com/docs/#configure-your-aws-credentials]

## SQLAlchemy

ClapDB incorporates a minimal SQLAlchemy implementation (without any ORM features) for compatibility with Superset. It has only been tested against SQLAlchemy versions 1.4.x, and is unlikely to work with more complex SQLAlchemy applications.

The interval type in ClapDB is implemented based on PostgreSQL, which calculation rule is special. Converting it to Python timedelta may result in information loss. Therefore, we return interval as string type.
