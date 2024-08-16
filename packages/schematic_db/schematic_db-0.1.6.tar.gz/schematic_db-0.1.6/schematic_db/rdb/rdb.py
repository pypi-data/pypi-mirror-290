"""RelationalDatabase"""

from abc import ABC, abstractmethod
import pandas as pd
from schematic_db.db_schema.db_schema import TableSchema


class InsertDatabaseError(Exception):
    """Raised when a database class catches an error doing an insert"""

    def __init__(self, table_name: str, sql_error: str | None = None) -> None:
        """
        Args:
            table_name (str): The name of the table being inserted into
            sql_error (str | None): An otpional SQL error message

        """
        self.message = "Error inserting/upserting dataframe into table:"
        self.table_name = table_name
        self.sql_error = sql_error
        super().__init__(self.message)

    def __str__(self) -> str:
        msg = f"{self.message}; Name: {self.table_name}"
        if self.sql_error is not None:
            msg = f"{msg}; Error: {self.sql_error}"
        return msg


class RelationalDatabase(ABC):
    """An interface for relational database types"""

    @abstractmethod
    def get_table_names(self) -> list[str]:
        """Gets the names of the tables in the database

        Returns:
            list[str]: A list of table names
        """

    @abstractmethod
    def get_table_schema(self, table_name: str) -> TableSchema:
        """Returns a TableSchema created from the current database table

        Args:
            table_name (str): The name of the table

        Returns:
            Optional[TableSchema]: The schema for the given table
        """

    @abstractmethod
    def execute_sql_query(self, query: str) -> pd.DataFrame:
        """Executes a valid SQL statement
        Should be used when a result is expected.


        Args:
            query (str): A SQL statement

        Returns:
            pd.DataFrame: The table
        """

    @abstractmethod
    def query_table(self, table_name: str) -> pd.DataFrame:
        """Queries a whole table

        Args:
            table_name (str): The name of the table

        Returns:
            pd.DataFrame: The table
        """

    @abstractmethod
    def add_table(self, table_schema: TableSchema) -> None:
        """Adds a table to the schema

        Args:
            table_schema (TableSchema): The schema for the table being added
        """

    @abstractmethod
    def drop_table(self, table_name: str) -> None:
        """Drops a table from the schema
        Args:
            table_name (str): The id(name) of the table to be dropped
        """

    @abstractmethod
    def drop_all_tables(self) -> None:
        """Drops all tables from the database"""

    @abstractmethod
    def insert_table_rows(self, table_name: str, data: pd.DataFrame) -> None:
        """Inserts rows into the given table

        Args:
            table_name (str): The name of the table the rows be upserted into
            data (pd.DataFrame): A pandas.DataFrame. It must contain the primary keys of the table
        """

    @abstractmethod
    def upsert_table_rows(self, table_name: str, data: pd.DataFrame) -> None:
        """Upserts rows into the given table

        Args:
            table_name (str): The name of the table the rows be upserted into
            data (pd.DataFrame): A pandas.DataFrame. It must contain the primary keys of the table
        """

    @abstractmethod
    def delete_table_rows(self, table_name: str, data: pd.DataFrame) -> None:
        """Deletes rows from the given table

        Args:
            table_name (str): The name of the table the rows will be deleted from
            data (pd.DataFrame): A pandas.DataFrame. It must contain the primary keys of the table
        """
