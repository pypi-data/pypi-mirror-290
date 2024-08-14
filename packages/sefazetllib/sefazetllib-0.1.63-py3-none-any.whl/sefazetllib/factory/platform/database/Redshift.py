from typing import Any, Dict, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from sefazetllib.factory.platform.DatabasePlatform import DatabasePlatform


class Redshift(DatabasePlatform):
    def __init__(self, name: str = "Redshift Job", configs: list = []) -> None:
        """
        Initializes the Redshift class with a given name and configuration.

        Args:
            name (str): The name of the Redshift job.
            configs (list): A list of configuration tuples or a dictionary.
        """
        self.name = name
        self.session = None
        self.conn = None
        self.transaction = None

        if configs:
            url_args = (
                configs
                if isinstance(configs, dict)
                else {config[0]: config[1] for config in configs}
            )

            user = url_args.get("user")
            password = url_args.get("password")
            host = url_args.get("host")
            port = url_args.get("port")
            instance = url_args.get("instance")

            connection_string = (
                f"redshift+psycopg2://{user}:{password}@{host}:{port}/{instance}"
            )
            try:
                self.session = create_engine(connection_string)
                self.create_connection(session=create_engine(connection_string))
            except SQLAlchemyError as err:
                raise RuntimeError(f"Error creating engine: {str(err)}")

    def get_url(self, **kwargs) -> str:
        """
        Constructs and returns a URL based on the provided parameters.

        Args:
            **kwargs: Keyword arguments containing host, port, file_format, operator, database, and instance.

        Returns:
            str: The constructed URL.
        """
        file_format = kwargs.get("file_format")
        operator = kwargs.get("operator")
        database = kwargs.get("database")
        host = kwargs.get("host")
        port = kwargs.get("port")
        instance = kwargs.get("instance")
        return f"{file_format}{operator}{database}:iam://{host}:{port}/{instance}"

    def get_table_name(self, **kwargs) -> str:
        """
        Constructs and returns a table name based on the provided schema and table.

        Args:
            **kwargs: Keyword arguments containing schema and table.

        Returns:
            str: The constructed table name.
        """
        schema = kwargs.get("schema")
        table = kwargs.get("table")
        return f"{schema}.{table}"

    def create_connection(self, session: Any) -> None:
        """
        Creates a connection to the database.

        Args:
            session (Any): An existing SQLAlchemy Engine or a mock object for testing.

        Raises:
            RuntimeError: If there is an error creating the connection.
        """
        try:
            self.conn = session.connect()
        except SQLAlchemyError as err:
            raise RuntimeError(f"Error creating connection: {str(err)}")

    def close_connection(self) -> None:
        """
        Closes the connection to the database.

        Raises:
            RuntimeError: If there is an error closing the connection.
        """
        try:
            if self.conn:
                self.conn.close()
        except SQLAlchemyError as err:
            raise RuntimeError(f"Error closing connection: {str(err)}")

    def begin_transaction(self) -> None:
        """
        Begins a transaction.
        """
        if self.conn:
            self.transaction = self.conn.begin()

    def create_commit(self) -> None:
        """
        Commits the current transaction.
        """
        if self.transaction is not None:
            self.transaction.commit()

    def rollback_transaction(self) -> None:
        """
        Rolls back the current transaction.
        """
        if self.transaction is not None:
            self.transaction.rollback()

    def delete_from_table(self, schema: str, table: str) -> None:
        """
        Deletes all records from the specified table.

        Args:
            schema (str): The schema of the table.
            table (str): The name of the table.
        """
        schema_table = self.get_table_name(schema=schema, table=table)
        delete_query = f"DELETE FROM {schema_table};"

        self.conn.execute(text(delete_query))

    def truncate_table(self, schema: str, table: str) -> None:
        """
        Truncates the specified table.

        Args:
            schema (str): The schema of the table.
            table (str): The name of the table.
        """
        schema_table = self.get_table_name(schema=schema, table=table)
        truncate_query = f"TRUNCATE TABLE {schema_table};"

        self.conn.execute(text(truncate_query))

    def create_table(
        self,
        table: str,
        source_schema: str,
        source_table: str,
        is_temporary: Optional[bool] = False,
        is_schema_only: Optional[bool] = False,
    ) -> None:
        """
        Creates a new table based on a source table.

        Args:
            table (str): The name of the new table.
            source_schema (str): The schema of the source table.
            source_table (str): The name of the source table.
            is_temporary (bool, optional): Whether the new table should be temporary.
            is_schema_only (bool, optional): Whether the new table should only include the schema.
        """
        create_table_query = f"""
            CREATE {"TEMP" if is_temporary else ""} TABLE {table} AS
            SELECT *
            FROM {source_schema}.{source_table}
            {"WHERE 1=0" if is_schema_only else ""};
        """

        self.conn.execute(text(create_table_query))

    def drop_table(self, schema: str, table: str) -> None:
        """
        Drops the specified table if it exists.

        Args:
            schema (str): The schema of the table.
            table (str): The name of the table.
        """
        schema_table = self.get_table_name(schema=schema, table=table)
        drop_query = f"DROP TABLE IF EXISTS {schema_table};"

        self.conn.execute(text(drop_query))

    def copy_table(
        self,
        table: str,
        data_source: str,
        iam_role: str,
        columns: Optional[list] = None,
        operation_options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Copies data from a source to a table using the specified format and IAM role.

        Args:
            table (str): The name of the target table.
            data_source (str): The source data location.
            iam_role (str): The IAM role for the copy operation.
            columns (list, optional): List of columns to copy. If None, all columns are copied.
            operation_options (dict, optional): Additional options for the copy operation.
                Supports the following keys:
                - 'copy':
                    - 'data_format' (str, optional): The data format of the source data (e.g., 'CSV', 'JSON').
                    - 'optional_parameters' (str, optional): Additional parameters for the COPY command
                    (e.g., 'DELIMITER ',' COMPUPDATE ON').

        Examples:
            copy_table(
                table='target_table',
                data_source='s3://bucket/path',
                iam_role='arn:aws:iam::123456789012:role/MyRedshiftRole',
                columns=['column1', 'column2'],
                operation_options={
                    'copy': {
                        'data_format': 'CSV',
                        'optional_parameters': 'DELIMITER \',\' IGNOREHEADER 1'
                    }
                }
            )
        """
        if operation_options is None:
            operation_options = {}

        data_format = operation_options.get("copy", {}).get("data_format")
        optional_parameters = operation_options.get("copy", {}).get(
            "optional_parameters"
        )

        copy_query = f"""
            COPY {table}
        """

        if columns:
            columns_str = ", ".join([f"{column}" for column in columns])
            copy_query += f"({columns_str})"

        copy_query += f"""
            FROM '{data_source}' IAM_ROLE '{iam_role}'
        """

        if data_format:
            copy_query += f" FORMAT AS {data_format}"

        if optional_parameters:
            copy_query += f" {optional_parameters}"

        self.conn.execute(text(copy_query))

    def merge_tables(
        self,
        target_schema: str,
        target_table: str,
        primary_key: str,
        columns: list,
        operation_options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Merges data from a source table into a target table.

        Args:
            target_schema (str): The schema of the target table.
            target_table (str): The name of the target table.
            primary_key (str): The primary key column for matching records.
            columns (list): List of columns to be merged.
            operation_options (dict, optional): Additional options for the merge operation.
                Supports the following keys:
                - 'merge':
                    - 'source_table' (str, required): The source table from which to merge data.
                    - 'delete_from_target' (bool, optional): If True, deletes records from the target table
                    that do not exist in the source table.
                    - 'delete_from_source' (bool, optional): If True, deletes records from the source table
                    that do not exist in the target table.
                    - 'delete_conditions' (list of str, optional): Additional conditions for deleting records.
                    - 'matched_update_columns' (list of str, optional): Specific columns to update when a match is found.
                    If None, all columns are updated.
                    - 'not_matched_insert_columns' (list of str, optional): Specific columns to insert when no match is found.
                    If None, all columns are inserted.
                    - 'extra_conditions' (list of str, optional): Additional conditions for the merge operation.

        Examples:
            merge_tables(
                target_schema='public',
                target_table='target_table',
                primary_key='id',
                columns=['id', 'name', 'value'],
                operation_options={
                    'merge': {
                        'source_table': 'source_table',
                        'delete_from_target': True,
                        'delete_from_source': False,
                        'delete_conditions': ['target_table.value IS NOT NULL'],
                        'matched_update_columns': ['name', 'value'],
                        'not_matched_insert_columns': ['id', 'name', 'value'],
                        'extra_conditions': ['source_table.active = 1']
                    }
                }
            )
        """
        if operation_options is None:
            operation_options = {}

        source_table = operation_options.get("merge", {}).get("source_table").lower()
        delete_from_target = operation_options.get("merge", {}).get(
            "delete_from_target"
        )
        delete_from_source = operation_options.get("merge", {}).get(
            "delete_from_source"
        )
        delete_conditions = operation_options.get("merge", {}).get("delete_conditions")
        matched_update_columns = operation_options.get("merge", {}).get(
            "matched_update_columns"
        )
        not_matched_insert_columns = operation_options.get("merge", {}).get(
            "not_matched_insert_columns"
        )
        extra_conditions = operation_options.get("merge", {}).get("extra_conditions")

        target_schema_table = self.get_table_name(
            schema=target_schema, table=target_table
        )

        def merge_delete_from_table(
            delete_from: str, using: str, primary_key: str
        ) -> None:
            delete_query = f"""
                DELETE FROM {delete_from} USING {using}
                WHERE {delete_from}.{primary_key} NOT IN (
                        SELECT {primary_key}
                        FROM {using}
                    )
            """

            if delete_conditions:
                for condition in delete_conditions:
                    delete_query += f"""
                        AND {condition}
                    """
            self.conn.execute(text(delete_query))

        if delete_from_target:
            merge_delete_from_table(
                delete_from=target_schema_table,
                using=source_table,
                primary_key=primary_key,
            )

        if delete_from_source:
            merge_delete_from_table(
                delete_from=source_table,
                using=target_schema_table,
                primary_key=primary_key,
            )

        update_set = ",".join([f"{column} = s.{column}" for column in columns])

        insert_columns = ",".join(columns)
        insert_values = ",".join([f"s.{column}" for column in columns])

        if matched_update_columns:
            update_set = ",".join(
                [f"{column} = s.{column}" for column in matched_update_columns]
            )

        if not_matched_insert_columns:
            insert_columns = ",".join(not_matched_insert_columns)
            insert_values = ",".join(
                [f"s.{column}" for column in not_matched_insert_columns]
            )

        merge_query = f"""
            MERGE INTO {target_schema_table} USING {source_table} AS s ON {target_table}.{primary_key} = s.{primary_key}
        """

        if extra_conditions:
            for condition in extra_conditions:
                merge_query += f"""
                    AND {condition}
                """

        merge_query += f"""
            WHEN MATCHED THEN
            UPDATE
            SET {update_set}
                WHEN NOT MATCHED THEN
            INSERT ({insert_columns})
            VALUES ({insert_values})
        """

        self.conn.execute(text(merge_query))

    def read(self) -> None:
        """
        Placeholder method for reading data. Needs implementation based on requirements.
        """
        pass

    def load(self) -> None:
        """
        Placeholder method for loading data. Needs implementation based on requirements.
        """
        pass
