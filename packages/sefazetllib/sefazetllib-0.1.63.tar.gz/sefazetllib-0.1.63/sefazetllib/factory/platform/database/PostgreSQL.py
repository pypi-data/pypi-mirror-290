from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine, text

from sefazetllib.factory.platform.DatabasePlatform import DatabasePlatform


class PostgreSQL(DatabasePlatform):
    def __init__(self, name="PostgreSQL Job", configs=[]) -> None:
        self.name = name
        self.session = None
        self.conn = None
        self.transaction = None

        if configs != []:
            url_args = configs
            if not isinstance(configs, dict):
                url_args = {config[0]: config[1] for config in configs}

            self.session = create_engine(
                f"postgresql+psycopg2://"
                f'{url_args["user"]}:{url_args["password"]}@{url_args["host"]}:'
                f'{url_args["port"]}/'
                f'{url_args["instance"]}'
            )
            self.create_connection()

    def get_url(self, **kwargs):
        host = kwargs["host"]
        port = kwargs["port"]
        file_format = kwargs["file_format"]
        operator = kwargs["operator"]
        database = kwargs["database"].lower()
        instance = kwargs["instance"]
        return f"{file_format}{operator}{database}://{host}:{port}/{instance}"

    def get_table_name(self, **kwargs):
        schema = kwargs["schema"]
        table = kwargs["table"]
        return f"{schema}.{table}"

    def create_connection(self):
        self.conn = self.session.connect()
        return

    def close_connection(self):
        self.conn.close()
        return

    def begin_transaction(self):
        self.transaction = self.conn.begin()
        return

    def create_commit(self):
        if self.transaction is not None:
            self.transaction.commit()
        return

    def rollback(self):
        if self.transaction is not None:
            self.transaction.rollback()
        return

    def truncate(self, **kwargs):
        schema = kwargs["schema"].lower()
        table = kwargs["table"].lower()
        self.conn.execute(text(f"TRUNCATE TABLE {schema}.{table};"))
        return

    def drop_constraints(self, **kwargs):
        table = kwargs["table"].lower()
        schema = kwargs["schema"].lower()
        dependencies = [
            row._asdict()
            for row in self.conn.execute(
                text(
                    f"""
                        SELECT tc.table_schema,
                            tc.constraint_name,
                            tc.table_name,
                            kcu.column_name,
                            ccu.table_schema AS foreign_table_schema,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM information_schema.table_constraints AS tc
                            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
                            AND tc.table_schema = kcu.table_schema
                            JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
                        WHERE tc.constraint_type = 'FOREIGN KEY'
                            AND (
                                tc.table_name = '{table}'
                                OR ccu.table_name = '{table}'
                            )
                            AND (
                                tc.table_schema = '{schema}'
                                OR ccu.table_schema = '{schema}'
                            );
                    """
                )
            ).fetchall()
        ]

        alter_queries = [
            f"ALTER TABLE {dependencie['table_schema']}.{dependencie['table_name']} DROP CONSTRAINT {dependencie['constraint_name']};"
            for dependencie in dependencies
        ]
        if bool(alter_queries):
            self.conn.execute(text("\n".join(alter_queries)))
        return dependencies

    def create_constraints(self, **kwargs):
        dependencies = kwargs["dependencies"]

        alter_queries = [
            f"""
                ALTER TABLE {dependencie['table_schema']}.{dependencie['table_name']}
                ADD CONSTRAINT {dependencie['constraint_name']} FOREIGN KEY ({dependencie['column_name']}) REFERENCES {dependencie['foreign_table_schema']}.{dependencie['foreign_table_name']}({dependencie['foreign_column_name']});
            """
            for dependencie in dependencies
        ]
        if bool(alter_queries):
            self.conn.execute(text("\n".join(alter_queries)))
        return

    def merge_temporary_table_with_conflict(self, **kwargs):
        schema = kwargs["schema"].lower()
        table = kwargs["table"].lower()
        temporary_schema = kwargs["temporary_schema"].lower()
        temporary_table = kwargs["temporary_table"].lower()
        columns = kwargs["columns"]
        sk_name = kwargs["sk_name"]

        try:
            self.begin_transaction()
            self.conn.execute(
                text(
                    f"""
                        INSERT INTO {schema }.{table} ({",".join(columns)})
                        SELECT {",".join(columns)}
                        FROM {temporary_schema}.{temporary_table} ON CONFLICT ({sk_name}) DO
                        UPDATE
                        SET {",".join([f"{col}=EXCLUDED.{col}" for col in columns])};
                    """
                )
            )

        except Exception as err:
            self.rollback()
            raise Exception(str(err))

        else:
            self.create_commit()
        return

    def insert_from_temporary_table(self, **kwargs):
        schema = kwargs["schema"].lower()
        table = kwargs["table"].lower()
        temporary_schema = kwargs["temporary_schema"].lower()
        temporary_table = kwargs["temporary_table"].lower()
        columns = kwargs["columns"]

        try:
            self.begin_transaction()
            self.conn.execute(
                text(
                    f"""
                        INSERT INTO {schema}.{table} ({",".join(columns)})
                        SELECT {",".join(columns)}
                        FROM {temporary_schema}.{temporary_table};
                    """
                )
            )

        except Exception as err:
            self.rollback()
            raise Exception(str(err))

        else:
            self.create_commit()

        return

    def delete_insert_from_temporary_table(self, **kwargs):
        schema = kwargs["schema"].lower()
        table = kwargs["table"].lower()
        temporary_schema = kwargs["temporary_schema"].lower()
        temporary_table = kwargs["temporary_table"].lower()
        columns = kwargs["columns"]
        sk_name = kwargs["sk_name"]

        try:
            self.begin_transaction()
            self.conn.execute(
                text(
                    f"""
                        DELETE FROM {schema}.{table} AS tb1 USING {temporary_schema}.{temporary_table} AS tb2
                        WHERE tb1.{sk_name} = tb2.{sk_name};
                    """
                )
            )
            self.conn.execute(
                text(
                    f"""
                        INSERT INTO {schema}.{table} ({",".join(columns)})
                        SELECT {",".join(columns)}
                        FROM {temporary_schema}.{temporary_table};
                    """
                )
            )

        except Exception as err:
            self.rollback()
            raise Exception(str(err))

        else:
            self.create_commit()

        return

    def delete_matched_temporary_table(self, **kwargs):
        schema = kwargs["schema"].lower()
        table = kwargs["table"].lower()
        temporary_schema = kwargs["temporary_schema"].lower()
        temporary_table = kwargs["temporary_table"].lower()
        sk_name = kwargs["sk_name"]

        try:
            self.begin_transaction()
            self.conn.execute(
                text(
                    f"""
                        DELETE FROM {schema}.{table} AS tb1 USING {temporary_schema}.{temporary_table} AS tb2
                        WHERE tb1.{sk_name} = tb2.{sk_name};
                    """
                )
            )

        except Exception as err:
            self.rollback()
            raise Exception(str(err))

        else:
            self.create_commit()
        return

    def drop_temporary_table(self, **kwargs):
        temporary_table = kwargs["temporary_table"].lower()
        temporary_schema = kwargs["temporary_schema"].lower()
        self.conn.execute(
            text(f"DROP TABLE IF EXISTS {temporary_schema}.{temporary_table};")
        )
        return

    def merge_tables(
        self,
        db_tables: Dict[str, str],
        primary_key: str,
        columns: List[str],
        operation_options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        This function merges two tables based on a primary key. It allows for deletion of records from the target and source tables,
        updating matched records, and inserting non-matched records. The operation options are specified in a dictionary.

        Args:
            db_tables (Dict[str, str]): A dictionary containing the schema and table names for the target and source tables.
            primary_key (str): The primary key on which the tables will be merged.
            columns (List[str]): The list of columns to be updated or inserted.
            operation_options (Optional[Dict[str, Any]], optional): A dictionary containing the operation options for the merge. Defaults to None. Can contain the following keys:
                - "merge": A dictionary that can contain the following keys:
                    - "delete_from_target": A boolean indicating whether to delete records from the target table that do not exist in the source table.
                    - "delete_from_source": A boolean indicating whether to delete records from the source table that do not exist in the target table.
                    - "delete_conditions": A list of conditions to be applied when deleting records. Each condition is a string that represents a SQL condition.
                    - "matched_update_columns": A list of column names to be updated in the target table when the records are matched. Defaults to all columns.
                    - "not_matched_insert_columns": A list of column names to be inserted in the target table when the records are not matched. Defaults to all columns.
                    - "extra_conditions": A list of extra conditions to be applied when merging the tables. Each condition is a string that represents a SQL condition.

        Examples:
            merge_tables(
                db_tables={
                    'target': {'schema': 'public', 'table': 'target_table'},
                    'source': {'schema': 'public', 'table': 'source_table'}
                },
                primary_key='id',
                columns=['id', 'name', 'value'],
                operation_options={
                    'merge': {
                        'delete_from_target': True,
                        'delete_from_source': False,
                        'delete_conditions': ['target_table.value IS NOT NULL'],
                        'matched_update_columns': ['name', 'value'],
                        'not_matched_insert_columns': ['id', 'name', 'value'],
                        'extra_conditions': ['source_table.active = 1']
                    }
                }
            )

        Returns:
            None
        """
        if not operation_options:
            operation_options = {}

        schema = db_tables["schema"]
        table = db_tables["table"]
        temporary_schema = db_tables["temporary_schema"]
        temporary_table = db_tables["temporary_table"]
        target_schema_table = self.get_table_name(schema=schema, table=table)
        source_schema_table = self.get_table_name(
            schema=temporary_schema, table=temporary_table
        )
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

        def merge_delete_from_table(delete_from: str, using: str, primary_key: str):
            delete_query = f"""
                 DELETE FROM {delete_from} AS t 
                 USING {using} AS s
                 WHERE t.{primary_key} NOT IN (
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
                using=source_schema_table,
                primary_key=primary_key,
            )

        if delete_from_source:
            merge_delete_from_table(
                delete_from=source_schema_table,
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
            MERGE INTO {target_schema_table} AS t
            USING {source_schema_table} AS s
            ON t.{primary_key} = s.{primary_key}
        """

        if extra_conditions:
            for condition in extra_conditions:
                merge_query += f"""
                    AND {condition}
                """
        merge_query += f"""
            WHEN MATCHED THEN
            UPDATE SET 
                {update_set}
            WHEN NOT MATCHED THEN
                INSERT ({insert_columns})
                VALUES ({insert_values})
        """

        self.conn.execute(text(merge_query))
        return

    def read(self, **kwargs):
        pass

    def load(self, **kwargs):
        pass
