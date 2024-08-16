"""
This module implement ClapDB http protocol to execute query and get meta.

code example:

    >>> client = Client("http", "localhost:8000", "user", "passwd", "db", 10.0)
    >>> meta_text = client.get_meta()
    >>> result_text = client.execute("select a, b, c from t")

The client return text which can be converted by json.loads.
"""

import requests

from clapdb import exceptions

GET_META_OPERATION = "GET_META"


class Client(object):
    """
    :param scheme: http or https
    :param netloc: host[:port]
    :param user: the user to execute operation
    :param passwd: the password of the user
    :param database: the database to execute operation
    :param timeout: how many seconds to wait for the server to send data before giving up, as a float
    """

    def __init__(
        self,
        scheme: str,
        netloc: str,
        user: str,
        passwd: str,
        database: str,
        timeout: float,
    ):
        self.scheme = scheme
        self.netloc = netloc
        self.user = user
        self.passwd = passwd
        self.database = database
        self.timeout = timeout

    def get_url(self):
        return "{scheme}://{netloc}".format(scheme=self.scheme, netloc=self.netloc)

    @property
    def url_for_query(self):
        return self.get_url() + "/psql?database=" + self.database

    @property
    def url_for_meta(self):
        return self.get_url() + "/meta?database=" + self.database

    def execute(self, sql):
        if sql == GET_META_OPERATION:
            return self.get_meta()

        try:
            resp = requests.post(
                self.url_for_query,
                data=sql,
                headers={
                    "Accept": "application/json",
                },
                auth=(self.user, self.passwd),
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as ex:
            raise exceptions.InterfaceError() from ex
        else:
            if resp.status_code == 400:
                raise exceptions.InterfaceError(resp.text)

            if resp.status_code != 200:
                raise exceptions.InternalError(resp.text)

            return resp.text

    def get_meta(self):
        try:
            resp = requests.get(
                self.url_for_meta,
                headers={
                    "Accept": "application/json",
                },
                auth=(self.user, self.passwd),
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as ex:
            raise exceptions.InterfaceError() from ex
        else:
            if resp.status_code == 400:
                raise exceptions.InterfaceError(resp.text)

            if resp.status_code != 200:
                raise exceptions.InternalError(resp.text)

            return resp.text
