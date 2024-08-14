import random
import string
from typing import Any, Dict, List, Optional

from sefazetllib.Builder import Builder, field
from sefazetllib.factory.platform.dataframe.Default import Default
from sefazetllib.factory.platform.Platform import Platform
from sefazetllib.factory.platform.PlatformFactory import PlatformFactory
from sefazetllib.load.Load import Load
from sefazetllib.utils.key import DefaultKey, Key


@Builder
class LoadDB(Load):
    platform: Platform = field(default=Default())
    database: str = field(default="")
    host: str = field(default="")
    port: int = field(default=0)
    instance: str = field(default="")
    schema: str = field(default="")
    table: str = field(default="")
    dbtable: str = field(default="")
    dbtable_temporary: str = field(default="")
    file_format: str = field(default="jdbc")
    driver: str = field(default="")
    url: str = field(default="")
    operator: str = field(default=":")
    authentication: Dict[str, Any] = field(default_factory=dict)
    reference: str = field(default="")
    df_writer: Any = field(default="")
    mode: str = field(default="")
    sk_name: str = field(default="")
    key: Key = field(default=DefaultKey())
    columns: List[str] = field(default_factory=list)
    operation: str = field(default="")
    operation_options: Dict[str, Any] = field(default_factory=dict)
    optional: bool = field(default=False)
    duplicates: bool = field(default=False)
    truncate: bool = field(default=False)
    load_date: bool = field(default=True)
    load_date_name: str = field(default="DAT_CARGA")
    load_date_timestamp: bool = field(default=False)
    load_date_timezone: str = field(default="UTC-3")
    fetch_size: int = field(default=100000)
    batch_size: int = field(default=100000)
    enable: bool = field(default=True)

    def set_platform(self, platform: Platform) -> None:
        """Set the platform if the default is used."""
        if isinstance(self.platform, Default):
            self.setPlatform(platform)

    def set_sk_name(self) -> None:
        """Set the surrogate key name based on the table name."""
        if self.sk_name == "":
            self.sk_name = f"SK_{self.table}"
            if "/" in self.table:
                table = self.table.split("/")[1]
                self.sk_name = f"SK_{table}"

    def get_database_platform(self) -> Platform:
        """Get the platform object for the database.

        Returns:
            Platform: The platform object.
        """
        return PlatformFactory(self.database).create(
            name="get url jdbc", configs=self.__build_properties()
        )

    def build_connection_string(self) -> None:
        """Build the JDBC connection string."""
        self.url = self.get_database_platform().get_url(
            file_format=self.file_format,
            operator=self.operator,
            database=self.database,
            host=self.host,
            port=self.port,
            instance=self.instance,
        )

    def set_table_names(self, platform_db: Platform) -> None:
        """Set the table and schema names.

        Args:
            platform_db (Platform): The platform database object.
        """
        random_string = self.__create_random_string(size=10)
        self.db_table_name = {
            "table": self.table.lower(),
            "schema": self.schema.lower(),
            "temporary_table": f"{self.table}_{random_string}".lower(),
            "temporary_schema": "temporario",
        }

        self.dbtable = platform_db.get_table_name(
            table=self.db_table_name["table"],
            schema=self.db_table_name["schema"],
        )

        self.dbtable_temporary = platform_db.get_table_name(
            table=self.db_table_name["temporary_table"],
            schema=self.db_table_name["temporary_schema"],
        )

    def __build_properties(self) -> Dict[str, Any]:
        """Build the properties dictionary for the platform.

        Returns:
            Dict[str, Any]: The properties dictionary.
        """
        return {
            "operation": self.operation,
            "file_format": self.file_format,
            "operator": self.operator,
            "database": self.database,
            "driver": self.driver,
            "user": self.authentication.get("user"),
            "password": self.authentication.get("password"),
            "dbtable": self.dbtable,
            "url": self.url,
            "host": self.host,
            "port": self.port,
            "instance": self.instance,
        }

    def __table_properties(self) -> Dict[str, str]:
        """Return the table properties.

        Returns:
            Dict[str, str]: The table properties.
        """
        return {"schema": self.schema, "table": self.table}

    def __is_postgresql(self) -> bool:
        """Check if the database is PostgreSQL.

        Returns:
            bool: True if PostgreSQL, False otherwise.
        """
        return self.database.lower() == "postgresql"

    def __is_redshift(self) -> bool:
        """Check if the database is Redshift.

        Returns:
            bool: True if Redshift, False otherwise.
        """
        return self.database.lower() == "redshift"

    def __is_merge_operation(self) -> bool:
        """Check if the operation is a merge.

        Returns:
            bool: True if merge operation, False otherwise.
        """
        return self.operation.lower() in ["merge", "merge_delete"]

    def __is_upsert_operation(self) -> bool:
        """Check if the operation is an upsert.

        Returns:
            bool: True if upsert operation, False otherwise.
        """
        return (
            "operation" in self.__build_properties()
            and self.__build_properties()["operation"] == "upsert"
        )

    def __is_insert_append(self) -> bool:
        """Check if the operation is an insert append.

        Returns:
            bool: True if insert append operation, False otherwise.
        """
        return self.operation.lower() == "insert" and self.mode.lower() == "append"

    def __is_copy_overwrite(self) -> bool:
        """Check if the operation is a copy overwrite.

        Returns:
            bool: True if copy overwrite operation, False otherwise.
        """
        return self.operation.lower() == "copy" and self.mode.lower() == "overwrite"

    def __is_copy_append(self) -> bool:
        """Check if the operation is a copy append.

        Returns:
            bool: True if copy append operation, False otherwise.
        """
        return self.operation.lower() == "copy" and self.mode.lower() == "append"

    def __is_merge_append(self) -> bool:
        """Check if the operation is a merge append.

        Returns:
            bool: True if merge append operation, False otherwise.
        """
        return self.operation.lower() == "merge" and self.mode.lower() == "append"

    def __prepare_columns_for_merge(self) -> None:
        """Prepare columns for merge operations."""
        self.columns = (
            [column.lower() for column in self.columns]
            if self.columns
            else [column.lower() for column in self.df_writer.columns]
        )
        self.sk_name = self.sk_name.lower()
        self.load_date_name = self.load_date_name.lower()

    def __create_random_string(self, size: int) -> str:
        """Create a random string of a given size.

        Args:
            size (int): The size of the random string.

        Returns:
            str: The random string.
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=size))

    def __create_constraints(
        self, dependencies: List[Any], platform_db: Platform
    ) -> None:
        """Create constraints on the database.

        Args:
            dependencies (List[Any]): List of dependencies.
            platform_db (Platform): The platform database object.

        Raises:
            Exception: If creating constraints fails.
        """
        platform_db.begin_transaction()

        try:
            platform_db.create_constraints(dependencies=dependencies)
        except Exception as err:
            platform_db.rollback()
            raise Exception(
                f"Transaction rolled back. Error creating constraints: {str(err)}"
            )
        else:
            platform_db.create_commit()

    def __drop_constraints(
        self, table_properties: Dict[str, str], platform_db: Platform
    ) -> List[Any]:
        """Drop constraints from the database.

        Args:
            table_properties (Dict[str, str]): The table properties.
            platform_db (Platform): The platform database object.

        Returns:
            List[Any]: List of dependencies.

        Raises:
            Exception: If dropping constraints fails.
        """
        platform_db.begin_transaction()

        try:
            dependencies = platform_db.drop_constraints(**table_properties)
        except Exception as err:
            platform_db.rollback()
            raise Exception(
                f"Transaction rolled back. Error dropping constraints: {str(err)}"
            )
        else:
            platform_db.create_commit()
        return dependencies

    def __create_cloud_storage_uri(
        self,
        provider: str,
        repository: str,
        layer: str,
        schema: str,
        entity: str,
        account_name: Optional[str] = "",
    ) -> str:
        """Create a URI for cloud storage.

        Args:
            provider (str): The cloud storage provider.
            repository (str): The repository name.
            layer (str): The layer name.
            schema (str): The schema name.
            entity (str): The entity name.
            account_name (str, optional): The account name for Azure Blob Storage.

        Returns:
            str: The cloud storage URI.

        Raises:
            ValueError: If the provider is unsupported or account_name is required but not provided.
        """
        if provider == "aws_s3":
            return f"s3://{repository}/{layer}/{schema}/{entity}"
        elif provider == "azure_blob":
            if not account_name:
                raise ValueError("account_name is required for Azure Blob Storage")
            return f"https://{account_name}.blob.core.windows.net/{repository}/{layer}/{schema}/{entity}"
        elif provider == "google_cloud_storage":
            return f"gs://{repository}/{layer}/{schema}/{entity}"
        else:
            raise ValueError("Unsupported cloud storage provider")

    def __handle_postgresql(
        self, platform_db: Platform, dependencies: List[Any]
    ) -> Any:
        """Handle PostgreSQL specific operations.

        Args:
            platform_db (Platform): The platform database object.
            dependencies (List[Any]): List of dependencies.

        Returns:
            Any: The loaded DataFrame.

        Raises:
            Exception: If there is an error during the PostgreSQL operations.
        """
        if self.__is_merge_operation():
            self.__prepare_columns_for_merge()

            df_loaded = self.__load_transaction(
                platform_db=platform_db,
                df=self.df_writer,
                sk_name=self.sk_name,
                truncate=self.truncate,
                mode=self.mode,
                dependencies=dependencies,
                dbtable=self.dbtable_temporary,
                load_date_name=self.load_date_name,
            )

            platform_db.begin_transaction()

            try:
                platform_db.merge_tables(
                    db_tables=self.db_table_name,
                    primary_key=self.sk_name,
                    columns=self.columns,
                    operation_options=self.operation_options,
                )

            except Exception as err:
                platform_db.rollback()
                raise Exception(
                    f"Transaction rolled back. Error in PostgreSQL merge/append process: {str(err)}"
                )
            else:
                platform_db.create_commit()
            finally:
                platform_db.begin_transaction()
                platform_db.drop_temporary_table(**self.db_table_name)
                platform_db.create_commit()

            return self.reference, df_loaded
        elif self.__is_insert_append():
            df_old = self.platform.create_df(self.columns)
        else:
            df_old = self.platform.read(
                file_format=self.file_format,
                url=platform_db.get_url(**self.__build_properties()),
                format_properties={
                    "driver": self.driver,
                    "user": self.authentication.get("user"),
                    "password": self.authentication.get("password"),
                    "dbtable": self.dbtable,
                    "fetchsize": self.fetch_size,
                },
                optional=False,
                columns="",
                duplicates=self.duplicates,
            )

        df_old = self.platform.columns_to_upper(df_old)

        if self.columns:
            df_old = self.platform.select_columns(df_old, self.columns)
            self.df_writer = self.platform.select_columns(self.df_writer, self.columns)

        df_old = self.platform.checkpoint(df_old)

        if self.__is_upsert_operation():
            self.df_writer = self.platform.union_by_name(
                left=self.platform.join(
                    left=df_old,
                    right=self.df_writer,
                    keys=self.sk_name,
                    how="left_anti",
                ),
                right=self.df_writer,
            )
            self.mode = "overwrite"
            self.truncate = True

        if not self.__is_insert_append():
            dependencies = self.__drop_constraints(
                table_properties=self.__table_properties(),
                platform_db=platform_db,
            )

        try:
            df_loaded = self.__load_transaction(
                platform_db=platform_db,
                df=self.df_writer,
                sk_name=self.sk_name,
                truncate=self.truncate,
                mode=self.mode,
                dependencies=dependencies,
                dbtable=self.dbtable,
                load_date_name=self.load_date_name,
            )
        except Exception as err:
            if not self.__is_insert_append():
                df_loaded = self.__load_transaction(
                    platform_db=platform_db,
                    df=df_old,
                    sk_name=self.sk_name,
                    truncate=True,
                    mode="overwrite",
                    dependencies=dependencies,
                    dbtable=self.dbtable,
                    load_date_name=self.load_date_name,
                )
            raise Exception(
                f"Error inserting data. Attempting to recover old information: {str(err)}"
            )

    def __handle_redshift(self, platform_db: Platform) -> Any:
        """Handle Redshift specific operations.

        Args:
            platform_db (Platform): The platform database object.

        Returns:
            Any: The loaded DataFrame.

        Raises:
            Exception: If there is an error during the Redshift operations.
        """
        try:
            provider = (
                self.operation_options.get("copy", {}).get("source_provider").lower()
            )
            repository = self.operation_options.get("copy", {}).get("source_repository")
            layer = self.operation_options.get("copy", {}).get("source_layer")
            schema = self.operation_options.get("copy", {}).get("source_schema")
            entity = self.operation_options.get("copy", {}).get("source_entity")
            account_name = self.operation_options.get("copy", {}).get(
                "source_account_name"
            )

            if self.__is_copy_overwrite():
                platform_db.begin_transaction()

                try:
                    platform_db.delete_from_table(
                        schema=self.schema.lower(), table=self.table.lower()
                    )

                    platform_db.copy_table(
                        table=self.dbtable.lower(),
                        data_source=self.__create_cloud_storage_uri(
                            provider=provider,
                            repository=repository,
                            layer=layer,
                            schema=schema,
                            entity=entity,
                            account_name=account_name,
                        ),
                        iam_role=self.authentication.get("iam_role"),
                        columns=self.columns,
                        operation_options=self.operation_options,
                    )
                except Exception as err:
                    platform_db.rollback_transaction()
                    raise Exception(
                        f"Transaction rolled back. Error in Redshift copy/overwrite process: {str(err)}"
                    )
                else:
                    platform_db.create_commit()
            elif self.__is_copy_append():
                platform_db.begin_transaction()

                try:
                    platform_db.copy_table(
                        table=self.dbtable.lower(),
                        data_source=self.__create_cloud_storage_uri(
                            provider=provider,
                            repository=repository,
                            layer=layer,
                            schema=schema,
                            entity=entity,
                            account_name=account_name,
                        ),
                        iam_role=self.authentication.get("iam_role"),
                        columns=self.columns,
                        operation_options=self.operation_options,
                    )
                except Exception as err:
                    platform_db.rollback_transaction()
                    raise Exception(
                        f"Transaction rolled back. Error in Redshift copy/append process: {str(err)}"
                    )
                else:
                    platform_db.create_commit()
            elif self.__is_merge_append():
                platform_db.begin_transaction()

                try:
                    platform_db.create_table(
                        table=f"{self.table.lower()}_temp",
                        source_schema=self.schema,
                        source_table=self.table,
                        is_temporary=True,
                        is_schema_only=True,
                    )

                    platform_db.copy_table(
                        table=f"{self.table.lower()}_temp",
                        data_source=self.__create_cloud_storage_uri(
                            provider=provider,
                            repository=repository,
                            layer=layer,
                            schema=schema,
                            entity=entity,
                            account_name=account_name,
                        ),
                        iam_role=self.authentication.get("iam_role"),
                        columns=self.columns,
                        operation_options=self.operation_options,
                    )

                    platform_db.merge_tables(
                        target_schema=self.schema.lower(),
                        target_table=self.table.lower(),
                        primary_key=self.sk_name.lower(),
                        columns=self.columns,
                        operation_options=self.operation_options,
                    )
                except Exception as err:
                    platform_db.rollback_transaction()
                    raise Exception(
                        f"Transaction rolled back. Error in Redshift merge/append process: {str(err)}"
                    )
                else:
                    platform_db.create_commit()

            else:
                raise Exception("Error in Redshift process (missing operation/mode)")

        except Exception as err:
            raise Exception(f"Error in Redshift process: {str(err)}")

        finally:
            platform_db.begin_transaction()
            platform_db.create_commit()

        return self.reference, self.df_writer

    def __load_transaction(
        self,
        platform_db: Platform,
        df: Any,
        sk_name: str,
        truncate: bool,
        mode: str,
        dependencies: List[Any],
        dbtable: str,
        load_date_name: str,
    ) -> Any:
        """Load data into the platform.

        Args:
            platform_db (Platform): The platform database object.
            df (Any): The DataFrame to load.
            sk_name (str): The surrogate key name.
            truncate (bool): Whether to truncate the table.
            mode (str): The loading mode.
            dependencies (List[Any]): List of dependencies.
            dbtable (str): The database table name.
            load_date_name (str): The load date column name.

        Returns:
            Any: The loaded DataFrame.

        Raises:
            Exception: If loading the transaction fails.
        """
        df_loaded = self.platform.load(
            df=df,
            sk_name=sk_name,
            key=self.key,
            columns=self.columns,
            duplicates=self.duplicates,
            file_format=self.file_format,
            format_properties={
                "driver": self.driver,
                "user": self.authentication.get("user"),
                "password": self.authentication.get("password"),
                "dbtable": dbtable,
                "truncate": truncate,
                "batchsize": self.batch_size,
            },
            url=platform_db.get_url(**self.__build_properties()),
            mode=mode,
            load_date=self.load_date,
            load_date_name=load_date_name,
            load_date_timestamp=self.load_date_timestamp,
            load_date_timezone=self.load_date_timezone,
        )

        if not self.__is_insert_append():
            self.__create_constraints(
                dependencies=dependencies, platform_db=platform_db
            )

        return df_loaded

    def execute(self, **kwargs) -> Any:
        """Execute the LoadDB process.

        Args:
            kwargs (dict): Additional arguments.

        Returns:
            tuple: Reference and DataFrame writer.

        Raises:
            Exception: If there is an error during execution.
        """
        # Only proceed if enable is True (default)
        if not self.enable:
            return (self.reference, self.df_writer)

        # Set the platform
        platform = kwargs.get("platform")
        self.set_platform(platform)

        # Define the sk_name
        self.set_sk_name()

        # Set the database platform object
        platform_db = self.get_database_platform()

        # Build the platform connection URL
        self.build_connection_string()

        # Set up table names
        self.set_table_names(platform_db)

        # Initialize DataFrame and dependencies
        df_loaded = self.df_writer
        dependencies = []

        # Handle different types of write operations
        try:
            if self.__is_postgresql():
                df_loaded = self.__handle_postgresql(platform_db, dependencies)
            elif self.__is_redshift():
                df_loaded = self.__handle_redshift(platform_db)
        except Exception as err:
            raise Exception(f"Error in LoadDB: {str(err)}")
        finally:
            platform_db.close_connection()

        self.platform.clean_checkpoint()

        return self.reference, df_loaded
