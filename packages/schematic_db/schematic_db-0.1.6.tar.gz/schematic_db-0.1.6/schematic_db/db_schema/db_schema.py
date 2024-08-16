"""DB schema
These are a set of classes for defining a database table in a dialect agnostic way.
"""

from enum import Enum
from typing import Any
from typing_extensions import Self
from pydantic.dataclasses import dataclass
from pydantic import field_validator, model_validator

from schematic_db.utils.validators import string_is_not_empty


class ColumnDatatype(Enum):
    """
    Either A generic datatype that should be supported by all database types,
    or a type specific to a certian type of database
    """

    # generic datatypes usable by any database
    TEXT = "text"
    DATE = "date"
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"
    # Synapse specific datatypes
    SYNAPSE_STRING = "synapse_string"
    SYNAPSE_FILE_HANDLE_ID = "synapse_file_handle_id"
    SYNAPSE_ENTITY_ID = "synapse_entity_id"
    SYNAPSE_LINK = "synapse_link"
    SYNAPSE_USER_ID = "synapse_user_id"
    SYNAPSE_STRING_LIST = "synapse_string_list"
    SYNAPSE_DATE_LIST = "synapse_date_list"
    SYNAPSE_INT_LIST = "synapse_int_list"
    SYNAPSE_BOOLEAN_LIST = "synapse_boolean_list"
    SYNAPSE_ENTITY_ID_LIST = "synapse_entity_id_list"
    SYNAPSE_USER_ID_LIST = "synapse_user_id_list"


@dataclass()
class ColumnSchema:
    """A schema for a table column (attribute)."""

    name: str
    datatype: ColumnDatatype
    required: bool = False
    index: bool = False
    string_size_max: int | None = None
    list_length_max: int | None = None
    _validate_name = field_validator("name")(string_is_not_empty)


@dataclass()
class ForeignKeySchema:
    """A foreign key in a database schema."""

    name: str
    foreign_table_name: str
    foreign_column_name: str

    _validate_name = field_validator("name")(string_is_not_empty)
    _validate_foreign_table_name = field_validator("foreign_table_name")(
        string_is_not_empty
    )
    _validate_foreign_column_name = field_validator("foreign_column_name")(
        string_is_not_empty
    )

    def get_column_dict(self) -> dict[str, str]:
        """Returns the foreign key in dict form

        Returns:
            dict[str, str]: A dictionary of the foreign key columns
        """
        return {
            "name": self.name,
            "foreign_table_name": self.foreign_table_name,
            "foreign_column_name": self.foreign_column_name,
        }


class TableColumnError(Exception):
    """A generic error involving table columns"""

    def __init__(self, message: str, table_name: str) -> None:
        """
        Args:
            message (str): A message describing the error
            table_name (str): The name of the table involved in the error
        """
        self.message = message
        self.table_name = table_name
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation"""
        return f"{self.message}: {self.table_name}"


class TableKeyError(Exception):
    """TableKeyError"""

    def __init__(self, message: str, table_name: str, key: str | None = None) -> None:
        """
        Args:
            message (str): A message describing the error
            table_name (str): The name of the table involved in the error
            key (Optional[str], optional): The name of the key involved in the error.
             Defaults to None.
        """
        self.message = message
        self.table_name = table_name
        self.key = key
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation"""
        return f"{self.message}: {self.table_name}; {self.key}"


@dataclass
class TableSchema:
    """A schema for a database table."""

    name: str
    columns: list[ColumnSchema]
    primary_key: str
    foreign_keys: list[ForeignKeySchema]

    _validate_name = field_validator("name")(string_is_not_empty)
    _validate_primary_key = field_validator("primary_key")(string_is_not_empty)

    @model_validator(mode="after")
    def check_self(self) -> Self:
        """Performs validation on whole object

        Returns:
            Self: The object itself
        """
        self.columns.sort(key=lambda x: x.name)
        self.foreign_keys.sort(key=lambda x: x.name)
        self._check_columns()
        self._check_primary_key()
        self._check_foreign_keys()
        return self

    def __eq__(self, other: Self) -> bool:  # type: ignore[override]
        """Overrides the default implementation"""
        return self.get_sorted_columns() == other.get_sorted_columns()

    def get_sorted_columns(self) -> list[ColumnSchema]:
        """Gets the tables columns sorted by name

        Returns:
            list[ColumnSchema]: Sorted list of columns
        """
        return sorted(self.columns, key=lambda x: x.name)

    def get_column_names(self) -> list[str]:
        """Returns a list of names of the columns

        Returns:
            List[str]: A list of names of the attributes
        """
        return [column.name for column in self.columns]

    def get_foreign_key_dependencies(self) -> list[str]:
        """Returns a list of table names the current table depends on

        Returns:
            list[str]: A list of table names
        """
        return [key.foreign_table_name for key in self.foreign_keys]

    def get_foreign_key_names(self) -> list[str]:
        """Returns a list of names of the foreign keys

        Returns:
            List[str]: A list of names of the foreign keys
        """
        return [key.name for key in self.foreign_keys]

    def get_foreign_key_by_name(self, name: str) -> ForeignKeySchema:
        """Returns foreign key

        Args:
            name (str): name of the foreign key

        Returns:
            ForeignKeySchema: The foreign key asked for
        """
        return [key for key in self.foreign_keys if key.name == name][0]

    def get_column_by_name(self, name: str) -> ColumnSchema:
        """Returns the column

        Args:
            name (str): name of the column

        Returns:
            ColumnSchema: The ColumnSchema asked for
        """
        return [column for column in self.columns if column.name == name][0]

    def _check_columns(self) -> None:
        """Checks that there are columns and they don't match

        Raises:
            TableColumnError: Raised when there are no columns
            TableColumnError: Raised when columns match
        """
        if len(self.columns) == 0:
            raise TableColumnError("There are no columns", self.name)
        if len(self.get_column_names()) != len(set(self.get_column_names())):
            raise TableColumnError("There are duplicate columns", self.name)

    def _check_primary_key(self) -> None:
        """Checks the primary is in the columns

        Raises:
            TableKeyError: Raised when the primary key is missing from the columns
        """
        if self.primary_key not in self.get_column_names():
            raise TableKeyError(
                "Primary key is missing from columns", self.name, self.primary_key
            )

    def _check_foreign_keys(self) -> None:
        """Checks each foreign key"""
        for key in self.foreign_keys:
            self._check_foreign_key(key)

    def _check_foreign_key(self, key: ForeignKeySchema) -> None:
        """Checks the foreign key exists in the columns and isn't referencing it's own table

        Args:
            key (ForeignKeySchema): A schema for a foreign key

        Raises:
            TableKeyError: Raised when the foreign key is missing from the columns
            TableKeyError: Raised when the foreign key references its own table
        """
        if key.name not in self.get_column_names():
            raise TableKeyError(
                "Foreign key is missing from columns", self.name, key.name
            )
        if key.foreign_table_name == self.name:
            raise TableKeyError(
                "Foreign key references its own table", self.name, key.name
            )


class SchemaMissingTableError(Exception):
    """When a foreign key references an table that doesn't exist"""

    def __init__(
        self, foreign_key: str, table_name: str, foreign_table_name: str
    ) -> None:
        """
        Args:
            foreign_key (str): The name of the foreign key
            table_name (str): The name of the table that the key is in
            foreign_table_name (str): The name of the table the key refers to that is missing
        """
        self.message = "Foreign key references table which does not exist in schema."
        self.foreign_key = foreign_key
        self.table_name = table_name
        self.foreign_table_name = foreign_table_name
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation"""
        msg = (
            f"Foreign key '{self.foreign_key}' in table '{self.table_name}' references table "
            f"'{self.foreign_table_name}' which does not exist in schema."
        )
        return msg


class SchemaMissingColumnError(Exception):
    """When a foreign key references an table column the table doesn't have"""

    def __init__(
        self,
        foreign_key: str,
        table_name: str,
        foreign_table_name: str,
        foreign_table_column: str,
    ) -> None:
        """
        Args:
            foreign_key (str): The name of the foreign key
            table_name (str): The name of the table that the key is in
            foreign_table_name (str): The name of the table the key refers
            foreign_table_column (str): The column in the foreign table that is missing
        """
        self.message = "Foreign key references column which does not exist."
        self.foreign_key = foreign_key
        self.table_name = table_name
        self.foreign_table_name = foreign_table_name
        self.foreign_table_column = foreign_table_column
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation"""
        msg = (
            f"Foreign key '{self.foreign_key}' in table '{self.table_name}' references "
            f"column '{self.foreign_table_column}' which does not exist in table "
            f"'{self.foreign_table_name}'"
        )
        return msg


@dataclass
class DatabaseSchema:
    """A database agnostic schema"""

    table_schemas: list[TableSchema]

    @model_validator(mode="after")
    def check_self(self) -> Self:
        """Performs validation on whole object

        Returns:
            Self: The object itself
        """
        for schema in self.table_schemas:
            self._check_foreign_keys(schema)
        return self

    def __eq__(self, other: Any) -> bool:
        """Overrides the default implementation"""
        return self.get_sorted_table_schemas() == other.get_sorted_table_schemas()

    def get_sorted_table_schemas(self) -> list[TableSchema]:
        """Gets the table schemas sorted by name

        Returns:
            list[TableSchema]: The list of sorted table schemas
        """
        return sorted(self.table_schemas, key=lambda x: x.name)

    def get_dependencies(self, table_name: str) -> list[str]:
        """Gets the tables dependencies

        Args:
            table_name (str): The name of the table

        Returns:
            list[str]: A list of tables names the table depends on
        """
        return self.get_schema_by_name(table_name).get_foreign_key_dependencies()

    def get_reverse_dependencies(self, table_name: str) -> list[str]:
        """Gets the names of the tables that depend on the input table

        Args:
            table_name (str): The name of the table

        Returns:
            list[str]: A list of table names that depend on the input table
        """
        return [
            schema.name
            for schema in self.table_schemas
            if table_name in schema.get_foreign_key_dependencies()
        ]

    def get_schema_names(self) -> list[str]:
        """Returns a list of names of the schemas

        Returns:
            List[str]: A list of names of the schemas
        """
        return [schema.name for schema in self.table_schemas]

    def get_schema_by_name(self, name: str) -> TableSchema:
        """Returns the schema

        Args:
            name (str): name of the schema

        Returns:
            TableSchema: The TableSchema asked for
        """
        return [schema for schema in self.table_schemas if schema.name == name][0]

    def _check_foreign_keys(self, schema: TableSchema) -> None:
        """Checks all foreign keys

        Args:
            schema (TableSchema): The schema of the table being checked
        """
        for key in schema.foreign_keys:
            self._check_foreign_key_table(schema, key)
            self._check_foreign_key_column(schema, key)

    def _check_foreign_key_table(
        self, schema: TableSchema, key: ForeignKeySchema
    ) -> None:
        """Checks that the table the foreign key refers to exists

        Args:
            schema (TableSchema): The schema for the table being checked
            key (ForeignKeySchema): The foreign key being checked

        Raises:
            SchemaMissingTableError: Raised when the table a foreign key references is missing
        """
        if key.foreign_table_name not in self.get_schema_names():
            raise SchemaMissingTableError(
                foreign_key=key.name,
                table_name=schema.name,
                foreign_table_name=key.foreign_table_name,
            )

    def _check_foreign_key_column(
        self, schema: TableSchema, key: ForeignKeySchema
    ) -> None:
        """Checks that the column the foreign key refers to exists

        Args:
            schema (TableSchema): The schema for the table being checked
            key (ForeignKeySchema): The foreign key being checked

        Raises:
            SchemaMissingColumnError: Raised when the column a foreign key references is missing
        """
        foreign_schema = self.get_schema_by_name(key.foreign_table_name)
        if key.foreign_column_name not in foreign_schema.get_column_names():
            raise SchemaMissingColumnError(
                foreign_key=key.name,
                table_name=schema.name,
                foreign_table_name=key.foreign_table_name,
                foreign_table_column=key.foreign_column_name,
            )
