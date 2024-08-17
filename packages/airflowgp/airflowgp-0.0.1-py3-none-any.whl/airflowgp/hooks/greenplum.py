from typing import Any, Dict

import pg8000.dbapi as gppy

from airflow.providers.common.sql.hooks.sql import DbApiHook

class GreenplumHook(DbApiHook):
    """
    General hook for jdbc db access.
    JDBC URL, username and password will be taken from the predefined connection.
    Note that the whole JDBC URL must be specified in the "host" field in the DB.
    Raises an airflow error if the given connection id doesn't exist.
    """

    conn_name_attr = 'gp_conn_id'
    default_conn_name = 'gp_default'
    conn_type = 'greenplum'
    hook_name = 'Greenplum Connection'
    supports_autocommit = True

    def get_conn(self) -> gppy.Connection:
        conn: Connection = self.connect(getattr(self, self.conn_name_attr))
        host: str = conn.host
        port: int = conn.port
        db: str = conn.description
        login: str = conn.login
        psw: str = conn.password

        conn = gppy.connect(user=login, password=psw, host=host, port=port, database=db)

        return conn

    def set_autocommit(self, conn: gppy.Connection, autocommit: bool) -> None:
        """
        Enable or disable autocommit for the given connection.
        :param conn: The connection.
        :param autocommit: The connection's autocommit setting.
        """
        conn.autocommit = autocommit

    def get_autocommit(self, conn: gppy.Connection) -> bool:
        """
        Get autocommit setting for the provided connection.
        Return True if conn.autocommit is set to True.
        Return False if conn.autocommit is not set or set to False
        :param conn: The connection.
        :return: connection autocommit setting.
        :rtype: bool
        """
        return conn.autocommit
