import random
import string
from typing import Any, Dict, List

from sefazetllib.Builder import Builder, field
from sefazetllib.factory.platform.dataframe.Default import Default
from sefazetllib.factory.platform.Platform import Platform
from sefazetllib.factory.platform.PlatformFactory import PlatformFactory
from sefazetllib.load.Load import Load
from sefazetllib.utils.key import DefaultKey, Key


@Builder
class LoadSQL(Load):
    platform: Platform = field(default=Default())
    file_format: str = field(default="jdbc")
    operator: str = field(default=":")
    host: str = field(default="")
    port: int = field(default=0)
    database: str = field(default="")
    instance: str = field(default="")
    dbtable: str = field(default="")
    driver: str = field(default="")
    schema: str = field(default="")
    table: str = field(default="")
    authentication: Dict[str, Any] = field(default_factory=dict)
    url: str = field(default="")
    reference: str = field(default="")
    df_writer: Any = field(default="")
    mode: str = field(default="")
    sk_name: str = field(default="")
    key: Key = field(default=DefaultKey())
    columns: List[str] = field(default_factory=list)
    operation: str = field(default="")
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

    def __build_properties(self):
        return {
            "operation": self.operation,
            "file_format": self.file_format,
            "operator": self.operator,
            "database": self.database,
            "driver": self.driver,
            "user": self.authentication["user"],
            "password": self.authentication["password"],
            "dbtable": self.dbtable,
            "url": self.url,
            "host": self.host,
            "port": self.port,
            "instance": self.instance,
        }

    def __table_properties(self):
        return {"schema": self.schema, "table": self.table}

    def __load_transaction(
        self,
        platform_db,
        df,
        sk_name,
        truncate,
        mode,
        dependencies,
        dbtable,
        load_date_name,
    ):
        df_loaded = self.platform.load(
            df=df,
            sk_name=sk_name,
            key=self.key,
            columns=self.columns,
            duplicates=self.duplicates,
            file_format=self.file_format,
            format_properties={
                "driver": self.driver,
                "user": self.authentication["user"],
                "password": self.authentication["password"],
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
        if not (self.operation.lower() == "insert" and mode.lower() == "append"):
            self.create_constraints(dependencies=dependencies, platform_db=platform_db)

        return df_loaded

    def build_connection_string(self):
        platform_db = PlatformFactory(self.database).create(
            name="get url jdbc", configs=self.__build_properties()
        )
        self.url = platform_db.get_url(
            file_format=self.file_format,
            operator=self.operator,
            database=self.database,
            host=self.host,
            instance=self.instance,
            schema=self.schema,
            port=self.port,
        )

        return platform_db

    def creat_random_string(self, **kwargs):
        return "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(kwargs["size"])
        )

    def create_constraints(self, **kwargs):
        dependencies = kwargs["dependencies"]
        platform_db = kwargs["platform_db"]
        platform_db.begin_transaction()
        try:
            platform_db.create_constraints(**{"dependencies": dependencies})
        except Exception as err:
            platform_db.rollback()
            raise Exception("Erro ao criar constraints", str(err))
        else:
            platform_db.create_commit()
        return

    def drop_constraints(self, **kwargs):
        table_properties = kwargs["table_properties"]
        platform_db = kwargs["platform_db"]
        platform_db.begin_transaction()
        try:
            dependencies = platform_db.drop_constraints(**table_properties)
        except Exception as err:
            platform_db.rollback()
            raise Exception(
                "Erro ao remover constraints. Realizando Rollback ...", str(err)
            )
        else:
            platform_db.create_commit()
        return dependencies

    def execute(self, **kwargs):
        if not self.enable:
            return (self.reference, self.df_writer)
        
        if isinstance(self.platform, Default):
            self.setPlatform(kwargs["platform"])

        if self.sk_name == "":
            self.sk_name = f"SK_{self.table}"
            if "/" in self.table:
                table = self.table.split("/")[1]
                self.sk_name = f"SK_{table}"

        platform_db = self.build_connection_string()
        self.db_table_name = {
            "table": self.table.lower(),
            "schema": self.schema.lower(),
            "temporary_table": f"{self.table}_{self.creat_random_string(size = 10)}".lower(),
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
        df_loaded = self.df_writer
        dependencies = []
        try:
            if (self.operation.lower() == "merge") | (
                self.operation.lower() == "merge_delete"
            ):
                
                self.columns = [c.lower() for c in self.columns] if self.columns else [c.lower() for c in self.df_writer.columns] 
                self.sk_name = self.sk_name.lower()
                self.load_date_name = self.load_date_name.lower()
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

                try:
                    if self.operation.lower() == "merge":
                        platform_db.merge_temporary_table_with_conflict(
                            **self.db_table_name,
                            columns=self.columns,
                            sk_name=self.sk_name,
                        )

                    if self.operation.lower() == "merge_delete":
                        dependencies = self.drop_constraints(
                            table_properties=self.db_table_name, platform_db=platform_db
                        )
                        platform_db.delete_insert_from_temporary_table(
                            **self.db_table_name,
                            columns=self.columns,
                            sk_name=self.sk_name,
                        )
                        self.create_constraints(
                            dependencies=dependencies, platform_db=platform_db
                        )

                except Exception as err:
                    raise Exception("Erro no processo de merge", str(err))

                finally:
                    platform_db.begin_transaction()
                    platform_db.drop_temporary_table(**self.db_table_name)
                    platform_db.create_commit()

                return self.reference, df_loaded

            if self.operation.lower() == "insert" and self.mode.lower() == "append":
                df_old = self.platform.create_df(self.columns)
            else:
                df_old = self.platform.read(
                    file_format=self.file_format,
                    url=platform_db.get_url(**self.__build_properties()),
                    format_properties={
                        "driver": self.driver,
                        "user": self.authentication["user"],
                        "password": self.authentication["password"],
                        "dbtable": self.dbtable,
                        "fetchsize": self.fetch_size,
                    },
                    optional=False,
                    columns="",
                    duplicates=self.duplicates,
                )

            df_old = self.platform.columns_to_upper(df_old)

            if bool(self.columns):
                df_old = self.platform.select_columns(df_old, self.columns)
                self.df_writer = self.platform.select_columns(
                    self.df_writer, self.columns
                )

            df_old = self.platform.checkpoint(df_old)

            if (
                "operation" in self.__build_properties()
                and self.__build_properties()["operation"] == "upsert"
            ):
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

            if not (
                self.operation.lower() == "insert" and self.mode.lower() == "append"
            ):
                dependencies = self.drop_constraints(
                    table_properties=self.__table_properties(), platform_db=platform_db
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
                if not (
                    self.operation.lower() == "insert" and self.mode.lower() == "append"
                ):
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
                    "Erro ao inserir os dados, tentando recuperar as informações antigas...",
                    str(err),
                )

        except Exception as err:
            raise Exception("Erro no LoadSQL ...", str(err))
        finally:
            platform_db.close_connection()

        self.platform.clean_checkpoint()

        return self.reference, df_loaded
