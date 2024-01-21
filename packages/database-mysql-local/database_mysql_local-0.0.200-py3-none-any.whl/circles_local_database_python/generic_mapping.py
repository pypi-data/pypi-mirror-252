import datetime

from logger_local.LoggerLocal import Logger

from .constants import logger_mapping_object
from .generic_crud import GenericCRUD
from .utils import validate_none_select_table_name

logger = Logger.create_logger(object=logger_mapping_object)


class GenericMapping(GenericCRUD):
    def __init__(self, default_schema_name: str = None,
                 default_table_name: str = None,
                 default_view_table_name: str = None,
                 default_id_column_name: str = None,
                 default_entity_name1: str = None,
                 default_entity_name2: str = None,
                 is_test_data: bool = False):
        super().__init__(default_schema_name=default_schema_name,
                         default_table_name=default_table_name, default_view_table_name=default_view_table_name,
                         default_id_column_name=default_id_column_name, is_test_data=is_test_data)
        self.default_schema_name = default_schema_name
        self.default_table_name = default_table_name
        self.default_view_table_name = default_view_table_name
        self.default_id_column_name = default_id_column_name
        self.default_entity_name1 = default_entity_name1
        self.default_entity_name2 = default_entity_name2

    def insert_mapping(self, entity_name1: str, entity_name2: str, entity_id1: int, entity_id2: int) -> int:
        """Inserts a new link between two entities and returns the id of the
          new row or -1 if an error occurred.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :return: The id of the new row or -1 if an error occurred.
        """
        logger.start(object={"entity_name1": entity_name1, "entity_name2": entity_name2, "entity_id1": entity_id1,
                             "entity_id2": entity_id2})

        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        combined_table_name = f"{entity_name1}_{entity_name2}_table"
        data_json = {
            f"{entity_name1}_id": entity_id1,
            f"{entity_name2}_id": entity_id2}
        self._validate_data_json(data_json)
        self._validate_table_name(entity_name1)
        validate_none_select_table_name(combined_table_name)
        columns = ','.join(data_json.keys())
        values = ','.join(['%s' for _ in data_json])
        insert_query = f"INSERT " \
                       f"INTO {self.schema_name}.{combined_table_name}({columns}) " \
                       f"VALUES ({values})"
        params = tuple(data_json.values())
        try:
            self.cursor.execute(insert_query, params)
            self.connection.commit()
            link_id = self.cursor.lastrowid()
            logger.end("Data inserted successfully.",
                       object={"link_id": link_id})
            return link_id
        except Exception as error:
            logger.exception(self._log_error_message(message="Error inserting data_json",
                                                     sql_statement=insert_query), object=error)
            logger.end()
            raise

    def delete_mapping_by_id(self, entity_name1: str, entity_name2: str, entity_id1: int, entity_id2: int) -> None:
        """ Deletes a link between two entities.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :return: None
        """
        logger.start(object={"entity_name1": entity_name1, "entity_name2": entity_name2, "entity_id1": entity_id1,
                             "entity_id2": entity_id2})

        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        combined_table_name = f"{entity_name1}_{entity_name2}_table"

        where = f"{entity_name1}_id=%s AND {entity_name2}_id=%s"
        params = (entity_id1, entity_id2)
        self._validate_table_name(combined_table_name)
        validate_none_select_table_name(combined_table_name)
        # TODO: this is duplicated code from generic crud, should be refactored
        update_query = f"UPDATE {self.schema_name}.{combined_table_name} " \
                       f"SET end_timestamp=CURRENT_TIMESTAMP() " \
                       f"WHERE {where}"
        try:
            self.cursor.execute(update_query, params)
            self.connection.commit()
            logger.end("Deleted successfully.")

        except Exception as e:
            logger.exception(
                self._log_error_message(message="Error while deleting", sql_statement=update_query), object=e)
            logger.end()
            raise

    def select_multi_mapping_tupel_by_id(self, entity_name1: str,
                                         entity_name2: str, entity_id1: int,
                                         entity_id2: int, select_clause_value: str = "*") -> list:
        """Selects a row from the database by id.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param select_clause_value: The columns to select.
        :return: A list of dictionaries representing the rows.
        """
        logger.start(object={"entity_name1": entity_name1,
                             "entity_name2": entity_name2,
                             "entity_id1": entity_id1,
                             "entity_id2": entity_id2,
                             "select_clause_value": select_clause_value})

        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        combined_table_name = f"{entity_name1}_{entity_name2}_table"
        where = f"{entity_name1}_id=%s AND {entity_name2}_id=%s"
        params = (entity_id1, entity_id2)
        self._validate_table_name(combined_table_name)
        validate_none_select_table_name(combined_table_name)
        select_query = f"SELECT {select_clause_value} " \
                       f"FROM {self.schema_name}.{combined_table_name} " \
                       f"WHERE {where}"
        try:
            self.cursor.execute(select_query, params)
            result = self.cursor.fetchall()
            result = [tuple(str(value) if isinstance(
                value, datetime.datetime) else value for value in row) for row in result]
            logger.end("Data selected successfully.",
                       object={"result": result})
            return result
        except Exception as e:
            logger.exception(
                self._log_error_message(message="Error selecting data",
                                        sql_statement=select_query), object=e)
            logger.end()
            raise

    def select_multi_mapping_dict_by_id(self, entity_name1: str,
                                        entity_name2: str, entity_id1: int,
                                        entity_id2: int, select_clause_value: str = "*") -> list:
        """Selects a row from the database by id.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param select_clause_value: The columns to select.
        :return: A list of dictionaries representing the rows.
        """
        logger.start(object={"entity_name1": entity_name1,
                             "entity_name2": entity_name2,
                             "entity_id1": entity_id1,
                             "entity_id2": entity_id2,
                             "select_clause_value": select_clause_value})

        try:
            result = self.select_multi_mapping_tupel_by_id(entity_name1=entity_name1, entity_name2=entity_name2,
                                                           entity_id1=entity_id1, entity_id2=entity_id2,
                                                           select_clause_value=select_clause_value)
            result = [dict(
                zip([column[0] for column in self.cursor.description()], row)) for row in result]
        except Exception as e:
            logger.exception("Error selecting data", object=e)
            logger.end()
            raise
        logger.end("Data selected successfully.",
                   object={"result": result})
        return result
