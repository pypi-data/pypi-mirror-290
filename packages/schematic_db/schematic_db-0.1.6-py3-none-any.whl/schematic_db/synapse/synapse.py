"""Synapse"""

from typing import Any
import os
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import synapseclient  # type: ignore
import pandas  # type: ignore


class SynapseTableNameError(Exception):
    """SynapseTableNameError"""

    def __init__(self, message: str, table_name: str) -> None:
        """
        Args:
            message (str): A message describing the error
            table_name (str): The name of the table
        """
        self.message = message
        self.table_name = table_name
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}:{self.table_name}"


class SynapseDeleteRowsError(Exception):
    """SynapseDeleteRowsError"""

    def __init__(self, message: str, table_id: str, columns: list[str]) -> None:
        """
        Args:
            message (str): A message describing the error
            table_id (str): The synapse id of the table
            columns (list[str]): A list of columns in the synapse table
        """
        self.message = message
        self.table_id = table_id
        self.columns = columns
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}; table_id:{self.table_id}; columns: {', '.join(self.columns)}"


class Synapse:  # pylint: disable=too-many-public-methods
    """
    The Synapse class handles interactions with a project in Synapse.
    """

    def __init__(
        self, auth_token: str, project_id: str, cache_root_dir: str | None = None
    ) -> None:
        """Init

        Args:
            auth_token (str): A Synapse auth_token
            project_id (str): A Synapse id for a project
            cache_root_dir( str | None): Where the directory of the synapse cache should be located
        """
        self.project_id = project_id
        syn = synapseclient.Synapse(cache_root_dir=cache_root_dir)
        syn.login(authToken=auth_token, silent=True)
        self.syn = syn

    def purge_cache(self) -> None:
        """purges the synapse cache"""
        self.syn.cache.purge(before_date=datetime.now())

    def list_files_in_cache(self) -> list[str]:
        """creates a flat list of all files in the cache"""
        return sum([f for _, _, f in os.walk(self.syn.cache.cache_root_dir)], [])

    def download_csv_as_dataframe(
        self, synapse_id: str, purge_cache: bool = False
    ) -> pandas.DataFrame:
        """Downloads a csv file form Synapse and reads it

        Args:
            synapse_id (str): The Synapse id of the file
            purge_cache (bool): If true the synapse cache is purged after downloading

        Returns:
            pandas.DataFrame: The file in dataframe form
        """
        entity = self.syn.get(synapse_id)
        df = pandas.read_csv(entity.path, keep_default_na=False, na_values="")
        if purge_cache:
            self.purge_cache()
        return df

    def get_table_names(self) -> list[str]:
        """Gets the names of the tables in the schema

        Returns:
            list[str]: A list of table names
        """
        tables = self._get_table_data()
        return [table["name"] for table in tables]

    def _get_table_data(self) -> list[dict[str, Any]]:
        """Gets the list of Synapse table entities for the project

        Returns:
            list[dict[str, Any]]: A list of all Synapse tables as dicts
        """
        project = self.syn.get(self.project_id)
        return list(self.syn.getChildren(project, includeTypes=["table"]))

    def get_table_column_names(self, table_name: str) -> list[str]:
        """Gets the column names from a synapse table

        Args:
            table_name (str): The name of the table

        Returns:
            list[str]: A list of column names
        """
        synapse_id = self.get_synapse_id_from_table_name(table_name)
        table = self.syn.get(synapse_id)
        columns = list(self.syn.getTableColumns(table))
        return [column.name for column in columns]

    def get_synapse_id_from_table_name(self, table_name: str) -> str:
        """Gets the synapse id from the table name

        Args:
            table_name (str): The name of the table

        Raises:
            SynapseTableNameError: When no tables match the name
            SynapseTableNameError: When multiple tables match the name

        Returns:
            str: A synapse id
        """
        tables = self._get_table_data()
        matching_tables = [table for table in tables if table["name"] == table_name]
        if len(matching_tables) == 0:
            raise SynapseTableNameError("No matching tables with name:", table_name)
        if len(matching_tables) > 1:
            raise SynapseTableNameError(
                "Multiple matching tables with name:", table_name
            )
        return matching_tables[0]["id"]

    def get_table_name_from_synapse_id(self, synapse_id: str) -> str:
        """Gets the table name from the synapse id

        Args:
            synapse_id (str): A synapse id

        Returns:
            str: The name of the table with the synapse id
        """
        tables = self._get_table_data()
        return [table["name"] for table in tables if table["id"] == synapse_id][0]

    def query_table(
        self, synapse_id: str, include_row_data: bool = False
    ) -> pandas.DataFrame:
        """Queries a whole table

        Args:
            synapse_id (str): The Synapse id of the table to delete
            include_row_data (bool): Include row_id and row_etag. Defaults to False.

        Returns:
            pandas.DataFrame: The queried table
        """
        query = f"SELECT * FROM {synapse_id}"
        return self.execute_sql_query(query, include_row_data)

    def execute_sql_query(
        self, query: str, include_row_data: bool = False
    ) -> pandas.DataFrame:
        """Execute a Sql query

        Args:
            query (str): A SQL statement that can be run by Synapse
            include_row_data (bool): Include row_id and row_etag. Defaults to False.

        Returns:
            pandas.DataFrame: The queried table
        """
        result = self.execute_sql_statement(query, include_row_data)
        table = pandas.read_csv(result.filepath)
        return table

    def execute_sql_statement(
        self, statement: str, include_row_data: bool = False
    ) -> synapseclient.table.CsvFileTable:
        """Execute a SQL statement

        Args:
            statement (str): A SQL statement that can be run by Synapse
            include_row_data (bool): Include row_id and row_etag. Defaults to False.

        Returns:
            synapseclient.table.CsvFileTable: The synapse table result from
              the provided statement
        """
        table = self.syn.tableQuery(
            statement, includeRowIdAndRowVersion=include_row_data
        )
        assert isinstance(table, synapseclient.table.CsvFileTable)
        return table

    def build_table(self, table_name: str, table: pandas.DataFrame) -> None:
        """Adds a table to the project based on the input table

        Args:
            table_name (str): The name fo the table
            table (pandas.DataFrame): A dataframe of the table
        """
        table_copy = table.copy(deep=False)
        project = self.syn.get(self.project_id)
        table_copy = synapseclient.table.build_table(table_name, project, table_copy)
        self.syn.store(table_copy)

    def add_table(self, table_name: str, columns: list[synapseclient.Column]) -> None:
        """Adds a synapse table

        Args:
            table_name (str): The name of the table to be added
            columns (list[synapseclient.Column]): The columns to be added
        """
        # create a dictionary with a key for every column, and value of an empty list
        values: dict[str, list] = {column.name: [] for column in columns}
        schema = synapseclient.Schema(
            name=table_name, columns=columns, parent=self.project_id
        )
        table = synapseclient.Table(schema, values)
        self.syn.store(table)

    def delete_table(self, synapse_id: str) -> None:
        """Deletes a Synapse table
        Args:
            synapse_id (str): The Synapse id of the table to delete
        """
        self.syn.delete(synapse_id)

    def replace_table(self, table_name: str, table: pandas.DataFrame) -> None:
        """
        Replaces synapse table with table made in table.
        The synapse id is preserved.

        Args:
            table_name (str): The name of the table to be replaced
            table (pandas.DataFrame): A dataframe of the table to replace to old table with
        """
        if table_name not in self.get_table_names():
            self.build_table(table_name, table)
        else:
            synapse_id = self.get_synapse_id_from_table_name(table_name)

            self.delete_all_table_rows(synapse_id)
            self.delete_all_table_columns(synapse_id)
            self.add_table_columns(synapse_id, synapseclient.as_table_columns(table))
            self.insert_table_rows(synapse_id, table)

    def insert_table_rows(self, synapse_id: str, data: pandas.DataFrame) -> None:
        """Insert table rows into Synapse table
        Args:
            synapse_id (str): The Synapse id of the table to add rows into
            data (pandas.DataFrame): The rows to be added.
        """
        table = self.syn.get(synapse_id)
        self.syn.store(synapseclient.Table(table, data))

    def upsert_table_rows(self, synapse_id: str, data: pandas.DataFrame) -> None:
        """Upserts rows from  the given table

        Args:
            synapse_id (str): The Synapse ID fo the table to be upserted into
            data (pandas.DataFrame): The table the rows will come from
        """
        self.syn.store(synapseclient.Table(synapse_id, data))

    def delete_table_rows(self, synapse_id: str, data: pandas.DataFrame) -> None:
        """Deletes rows from the given table

        Args:
            synapse_id (str): The Synapse id of the table the rows will be deleted from
            data (pandas.DataFrame): A pandas.DataFrame. Columns must include "ROW_ID",
             and "ROW_VERSION"

        Raises:
            SynapseDeleteRowsError: If "ROW_ID" not in the columns of the data
            SynapseDeleteRowsError: If "ROW_VERSION" not in the columns of the data
        """
        columns = list(data.columns)
        if "ROW_ID" not in columns:
            raise SynapseDeleteRowsError(
                "ROW_ID missing from input data", synapse_id, columns
            )
        if "ROW_VERSION" not in columns:
            raise SynapseDeleteRowsError(
                "ROW_VERSION missing from input data", synapse_id, columns
            )
        self.syn.delete(synapseclient.Table(synapse_id, data))

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(synapseclient.core.exceptions.SynapseHTTPError),
    )
    def delete_all_table_rows(self, synapse_id: str) -> None:
        """Deletes all rows in the Synapse table

        Args:
            synapse_id (str): The Synapse id of the table
        """
        table = self.syn.get(synapse_id)
        columns = self.syn.getTableColumns(table)
        if len(list(columns)) > 0:
            results = self.syn.tableQuery(f"select * from {synapse_id}")
            self.syn.delete(results)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(synapseclient.core.exceptions.SynapseHTTPError),
    )
    def delete_all_table_columns(self, synapse_id: str) -> None:
        """Deletes all columns in the Synapse table

        Args:
            synapse_id (str): The Synapse id of the table
        """
        table = self.syn.get(synapse_id)
        columns = self.syn.getTableColumns(table)
        for col in columns:
            table.removeColumn(col)
        self.syn.store(table)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(synapseclient.core.exceptions.SynapseHTTPError),
    )
    def add_table_columns(
        self, synapse_id: str, columns: list[synapseclient.Column]
    ) -> None:
        """Add columns to synapse table

        Args:
            synapse_id (str): The Synapse id of the table to add the columns to
            columns (list[synapseclient.Column]): The columns to be added
        """
        table = self.syn.get(synapse_id)
        for col in columns:
            table.addColumn(col)
        self.syn.store(table)

    def get_entity_annotations(self, synapse_id: str) -> synapseclient.Annotations:
        """Gets the annotations for the Synapse entity

        Args:
            synapse_id (str): The Synapse id of the entity

        Returns:
            synapseclient.Annotations: The annotations of the Synapse entity in dict form.
        """
        return self.syn.get_annotations(synapse_id)

    def set_entity_annotations(
        self, synapse_id: str, annotations: dict[str, Any]
    ) -> None:
        """Sets the entities annotations to the input annotations

        Args:
            synapse_id (str): The Synapse ID of the entity
            annotations (dict[str, Any]): A dictionary of annotations
        """
        entity_annotations = self.syn.get_annotations(synapse_id)
        entity_annotations.clear()
        for key, value in annotations.items():
            entity_annotations[key] = value
        self.syn.set_annotations(entity_annotations)

    def clear_entity_annotations(self, synapse_id: str) -> None:
        """Removes all annotations from the entity

        Args:
            synapse_id (str): The Synapse ID of the entity
        """
        annotations = self.syn.get_annotations(synapse_id)
        annotations.clear()
        self.syn.set_annotations(annotations)
