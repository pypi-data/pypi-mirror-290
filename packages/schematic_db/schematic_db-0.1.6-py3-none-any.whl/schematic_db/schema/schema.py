"""Schema class"""

# pylint: disable=duplicate-code

import warnings
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from schematic_db.db_schema.db_schema import (
    DatabaseSchema,
    TableSchema,
    ForeignKeySchema,
    ColumnSchema,
    ColumnDatatype,
)
from schematic_db.utils.api_utils import (
    find_class_specific_properties,
    get_property_label_from_display_name,
    is_node_required,
    get_node_validation_rules,
    SchematicAPIError,
    SchematicAPITimeoutError,
)
from schematic_db.schema_graph.schema_graph import SchemaGraph
from schematic_db.utils.types import DisplayLabelType
from schematic_db.utils.validators import is_valid_url, is_data_model_file
from .database_config import DatabaseConfig


class NoColumnsWarning(Warning):
    """
    Occurs when a database table has no columns returned from find_class_specific_properties().
    """

    def __init__(self, message: str) -> None:
        """
        Args:
            message (str): A message describing the error
        """
        self.message = message
        super().__init__(self.message)


class MoreThanOneTypeRule(Exception):
    """Raised when an column has more than one validation type rule"""

    def __init__(
        self,
        column_name: str,
        type_rules: list[str],
    ):
        """
        Args:
            column_name (str): The name of the column
            type_rules (list[str]): A list of the type rules
        """
        self.message = "Attribute has more than one validation type rule"
        self.column_name = column_name
        self.type_rules = type_rules
        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"{self.message}; column name:{self.column_name}; "
            f"type_rules:{self.type_rules}"
        )


class ColumnSchematicError(Exception):
    """Raised when there is an issue getting data from the Schematic API for a column"""

    def __init__(
        self,
        column_name: str,
        table_name: str,
    ):
        """
        Args:
            column_name (str): The name of the column
            table_name (str): The name of the table
        """
        self.message = (
            "There was an issue getting data from the Schematic API for the column"
        )
        self.column_name = column_name
        self.table_name = table_name
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: column name: {self.column_name}; table_name: {self.table_name}"


@dataclass()
class SchemaConfig:
    """
    A config for a Schema.
    Properties:
        schema_url (str): A url to the jsonld schema file
        display_label_type (DisplayLabelType): The type of label used for display purposes
    """

    schema_url: str
    display_label_type: DisplayLabelType = "class_label"

    _validate_url = field_validator("schema_url")(is_valid_url)
    _validate_url2 = field_validator("schema_url")(is_data_model_file)


class Schema:
    """
    The Schema class interacts with the Schematic API to create a DatabaseSchema
     table.
    """

    def __init__(
        self,
        config: SchemaConfig,
        database_config: DatabaseConfig = DatabaseConfig([]),
    ) -> None:
        """
        The Schema class handles interactions with the schematic API.
        The main responsibilities are creating the database schema, and retrieving manifests.

        Args:
            config (SchemaConfig): A config describing the basic inputs for the schema table
            database_config (DatabaseConfig): Experimental and will be deprecated in the near
             future. A config describing optional database specific columns.

        """
        self.database_config = database_config
        self.schema_url = config.schema_url
        self.display_label_type = config.display_label_type
        self.schema_graph = SchemaGraph(config.schema_url, config.display_label_type)
        self.database_schema: DatabaseSchema | None = None

    def get_database_schema(self) -> DatabaseSchema:
        """Gets the current database schema

        Returns:
            DatabaseSchema: the current database schema
        """
        # When first initialized, database schema is None
        if self.database_schema is None:
            self.update_database_schema()
        assert self.database_schema is not None
        return self.database_schema

    def update_database_schema(self) -> None:
        """Updates the database schema."""
        table_names = self.schema_graph.create_sorted_table_name_list()
        table_schemas = [
            schema
            for schema in [self._create_table_schema(name) for name in table_names]
            if schema is not None
        ]
        self.database_schema = DatabaseSchema(table_schemas)

    def _create_table_schema(self, table_name: str) -> TableSchema | None:
        """Creates the the schema for one table in the database, if any column
         schemas can be created.

        Args:
            table_name (str): The name of the table the schema will be created for.

        Returns:
            Optional[TableSchema]: The config for the table if the table has columns
              otherwise None.
        """
        # Some components will not have any columns for various reasons
        columns = self._create_column_schemas(table_name)
        if not columns:
            return None

        return TableSchema(
            name=table_name,
            columns=columns,
            primary_key=self._get_primary_key(table_name),
            foreign_keys=self._get_foreign_keys(table_name),
        )

    def _create_column_schemas(
        self,
        table_name: str,
    ) -> list[ColumnSchema] | None:
        """Create the column schemas for the table, if any can be created.

        Args:
            table_name (str): The name of the table to create the column schemas for

        Returns:
            list[ColumnSchema] | None: A list of columns in ColumnSchema form
        """
        # the names of the columns to be created, in label(not display) form
        column_names = find_class_specific_properties(
            self.schema_url, table_name, self.display_label_type
        )
        columns = [
            self._create_column_schema(name, table_name) for name in column_names
        ]
        # Some Tables will not have any columns for various reasons
        if not columns:
            warnings.warn(
                NoColumnsWarning(
                    f"Table {table_name} has no columns, and will be skipped."
                )
            )
            return None
        return columns

    def _create_column_schema(self, column_name: str, table_name: str) -> ColumnSchema:
        """Creates a schema for  column

        Args:
            column_name (str): The name of the column
            table_name (str): The name of the table

        Returns:
            ColumnSchema: The schema for the column
        """
        column = self.database_config.get_column(table_name, column_name)

        # first the config is checked for datatype
        # and if not there, gotten from schematic
        datatype = (
            column.datatype
            if column and column.datatype is not None
            else self._get_column_datatype(column_name, table_name)
        )
        # first the config is checked for if the column is required,
        # and if not there, gotten from schematic
        required = (
            column.required
            if column and column.required is not None
            else self._is_column_required(column_name, table_name)
        )
        # first the config is checked for if the column should be indexed,
        # and if not there, defaults to false
        index = column.index if column and column.index is not None else False
        # check if config exists, and if not default to None for both max values
        string_size_max = column.string_size_max if column else None
        list_length_max = column.list_length_max if column else None

        return ColumnSchema(
            name=column_name,
            datatype=datatype,
            required=required,
            index=index,
            string_size_max=string_size_max,
            list_length_max=list_length_max,
        )

    def _is_column_required(self, column_name: str, table_name: str) -> bool:
        """Determines if the column is required in the schema

        Args:
            column_name (str): The name of the column
            table_name (str): The name of the table

        Raises:
            ColumnSchematicError: Raised when there is an issue with getting a result from the
             schematic API

        Returns:
            bool: Is the column required?
        """
        try:
            is_column_required = is_node_required(
                self.schema_url, column_name, self.display_label_type
            )
        except (SchematicAPIError, SchematicAPITimeoutError) as exc:
            raise ColumnSchematicError(column_name, table_name) from exc
        return is_column_required

    def _get_column_datatype(self, column_name: str, table_name: str) -> ColumnDatatype:
        """Gets the datatype for the column

        Args:
            column_name (str): The name of the column
            table_name (str): The name of the table

        Raises:
            ColumnSchematicError: Raised when there is an issue with getting a result from the
             schematic API
            MoreThanOneTypeRule: Raised when the Schematic API returns more than one rule that
             indicate the columns datatype

        Returns:
            ColumnDatatype: The columns datatype
        """
        datatypes = {
            "str": ColumnDatatype.TEXT,
            "float": ColumnDatatype.FLOAT,
            "num": ColumnDatatype.FLOAT,
            "int": ColumnDatatype.INT,
            "date": ColumnDatatype.DATE,
        }
        # Try to get validation rules from Schematic API
        try:
            all_validation_rules = get_node_validation_rules(
                self.schema_url, column_name, self.display_label_type
            )
        except (SchematicAPIError, SchematicAPITimeoutError) as exc:
            raise ColumnSchematicError(column_name, table_name) from exc
        # Try to get type from validation rules
        type_validation_rules = [
            rule for rule in all_validation_rules if rule in datatypes
        ]
        if len(type_validation_rules) > 1:
            raise MoreThanOneTypeRule(column_name, type_validation_rules)
        if len(type_validation_rules) == 1:
            return datatypes[type_validation_rules[0]]

        # Default to text if there are no validation type rules
        return ColumnDatatype.TEXT

    def _get_primary_key(self, table_name: str) -> str:
        """Get the primary key for the column

        Args:
            table_name (str): The name of the column

        Returns:
            str: The primary key of the column
        """
        # Attempt to get the primary key from the config
        primary_key_attempt = self.database_config.get_primary_key(table_name)
        # Check if the primary key is in the config, otherwise assume "id"
        if primary_key_attempt is None:
            return "id"

        return primary_key_attempt

    def _get_foreign_keys(self, table_name: str) -> list[ForeignKeySchema]:
        """Gets a list of foreign keys for an table in the database

        Args:
            table_name (str): The name of the table the config will be created for.

        Returns:
            list[ForeignKeySchema]: A list of foreign keys for the table.
        """
        # Attempt to get foreign keys from config
        foreign_keys_attempt = self.database_config.get_foreign_keys(table_name)
        # If there are no foreign keys in config use schema graph to create foreign keys
        if foreign_keys_attempt is None:
            return self._create_foreign_keys(table_name)

        return foreign_keys_attempt

    def _create_foreign_keys(self, table_name: str) -> list[ForeignKeySchema]:
        """Create a list of foreign keys an table in the database using the schema graph

        Args:
            table_name (str): The name of the table

        Returns:
            list[ForeignKeySchema]: A list of foreign
        """
        # Uses the schema graph to find tables the current table depends on
        parent_table_names = self.schema_graph.get_neighbors(table_name)
        # Each parent of the current table needs a foreign key to that parent
        return [self._create_foreign_key(name) for name in parent_table_names]

    def _create_foreign_key(self, foreign_table_name: str) -> ForeignKeySchema:
        """Creates a foreign key table

        Args:
            foreign_table_name (str): The name of the table the foreign key is referring to.

        Returns:
            ForeignKeySchema: A foreign key table.
        """
        # Assume the foreign key name is <table_name>_id where the table name is the
        #  name of the table the column the foreign key is in
        column_name = self._get_column_name(f"{foreign_table_name}_id")

        attempt = self.database_config.get_primary_key(foreign_table_name)
        foreign_column_name = "id" if attempt is None else attempt

        return ForeignKeySchema(column_name, foreign_table_name, foreign_column_name)

    def _get_column_name(self, column_name: str) -> str:
        """Gets the column name of a manifest column

        Args:
            column_name (str): The name of the column

        Returns:
            str: The column name of the column
        """
        return get_property_label_from_display_name(column_name)
