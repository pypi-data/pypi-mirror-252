import os

import mysql.connector  # noqa E402
from dotenv import load_dotenv
from logger_local.Logger import Logger  # noqa E402
from logger_local.LoggerComponentEnum import LoggerComponentEnum  # noqa E402

# TODO Move to Constants.py
from .cursor import (DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_ID,
                     DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_NAME,
                     DEVELOPER_EMAIL, Cursor)

load_dotenv()

obj = {
    'component_id': DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=obj)
connections_pool = {}


class Connector:
    @staticmethod
    def connect(schema_name: str):
        logger.start(object={"schema_name": schema_name})
        if (schema_name in connections_pool and
                connections_pool[schema_name] and
                connections_pool[schema_name].connection):
            if connections_pool[schema_name].connection.is_connected():
                logger.end("Return existing connections_pool", object={
                    'connections_pool': str(connections_pool[schema_name])})
                return connections_pool[schema_name]
            else:
                # reconnect
                connections_pool[schema_name].connection.reconnect()
                # TODO We should develop retry mechanism to support password rotation and small network issues.
                if connections_pool[schema_name].connection.is_connected():
                    logger.end("Reconnected successfully", object={
                        'connections_pool': str(connections_pool[schema_name])})
                    return connections_pool[schema_name]
                else:
                    connector = Connector(schema_name)
                    connections_pool[schema_name] = connector
                    logger.error("Reconnect failed, returning a new connection",
                                 object={'connections_pool': str(connections_pool[schema_name])})

                    return connector._connect_to_db()
        else:
            connector = Connector(schema_name)
            connections_pool[schema_name] = connector
            logger.end("Return connections_pool with a new connector",
                       object={'connector': str(connector)})
            return connector._connect_to_db()

    def __init__(self, schema_name, host=None, user=None, password=None) -> None:
        if not all([os.getenv("RDS_HOSTNAME"), os.getenv("RDS_USERNAME"), os.getenv("RDS_PASSWORD")]):
            error_message = "Error: Add RDS_HOSTNAME, RDS_USERNAME and RDS_PASSWORD to .env"
            logger.error(error_message)
            raise Exception(error_message)

        self.host = host or os.getenv("RDS_HOSTNAME")
        self.schema = os.getenv("RDS_DATABASE") or schema_name
        self.user = user or os.getenv("RDS_USERNAME")
        self.password = password or os.getenv("RDS_PASSWORD")

        # Checking RDS_HOSTNAME suffix
        if not (self.host.endswith("circ.zone") or self.host.endswith("circlez.ai")):
            logger.error(
                f"Warning: Your RDS_HOSTNAME={self.host} which is not what is expected")
        self.connection: mysql.connector = None
        self._cursor = None
        logger.end()

    def reconnect(self):
        logger.start("connect Attempting to reconnect...")
        try:
            self.connection.reconnect()
            self._cursor = self.connection.cursor()
            try:
                self._cursor.execute(f"USE `{self.schema}`;")
                logger.info(f"set schema to database: {self.schema}")
            except mysql.connector.Error as err:
                logger.exception(object=err)
                logger.end()
                raise
            logger.info("connect reconnected successfully!")
        except mysql.connector.Error as err:
            logger.exception("Coudn't connect to the database host=" +
                             self.host + " user=" + self.user, object=err)
            logger.end()
            raise
        logger.end(object={"self": str(self)})
        return self

    def _connect_to_db(self):
        logger.start("connect Attempting to connect...")
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.schema
            )
            self._cursor = self.connection.cursor()
            try:
                # We must have `` around {self.schema}
                # to support schema name using reserved words such as databae, group ...
                self._cursor.execute(f"USE `{self.schema}`;")
                logger.info(f"set schema to database: {self.schema}")
            except mysql.connector.Error as err:
                logger.exception(object=err)
                logger.end()
                raise
            logger.info("connect Connected successfully!")
        except mysql.connector.Error as err:
            logger.exception("Coudn't connect to the database host=" +
                             self.host + " user=" + self.user, object=err)
            logger.end()
            raise
        logger.end(object={"self": str(self)})
        return self

    def close(self) -> None:
        logger.start()
        try:
            if self._cursor:
                self._cursor.close()
                logger.info("Cursor closed successfully.")
        except Exception as e:
            logger.exception(object=e)

        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("Connection closed successfully.")
        except Exception as e:
            logger.exception("connection.py close()", object=e)
        logger.end()

    def cursor(self, dictionary=False, buffered=False) -> Cursor:
        logger.start("cursor asked", object={
            "dictionary": dictionary, "buffered": buffered})
        cursor_instance = Cursor(self.connection.cursor(
            dictionary=dictionary, buffered=buffered))
        logger.end("Cursor created successfully", object={
            "cursor_instance": str(cursor_instance)})
        return cursor_instance

    def commit(self) -> None:
        logger.start("commit to database")
        self.connection.commit()
        logger.end(object={})

    def set_schema(self, new_schema) -> None:
        if self.schema == new_schema:
            logger.info(f"Schema is already {new_schema}. No need to switch to it.")
            return
        logger.start()
        self.schema = new_schema
        if self.connection and self.connection.is_connected():
            try:
                use_schema = f"`{new_schema}`" if not new_schema.startswith("`") else new_schema
                self._cursor.execute(f"USE {use_schema};")
                logger.info(f"Switched to database: {new_schema}")
            except mysql.connector.Error as err:
                logger.exception(object=err)
                raise
        else:
            logger.error(
                "Connection is not established. The database will be used on the next connect.")
        logger.end()

    def rollback(self):
        logger.start()
        self.connection.rollback()
        logger.end()

    def start_tranaction(self):
        logger.start()
        self.connection.start_transaction()
        logger.end()
