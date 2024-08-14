import warnings
from typing import Any, Dict, List
from itertools import product

from sefazetllib.Builder import Builder, field
from sefazetllib.extract.Extract import Extract
from sefazetllib.factory.platform.dataframe.Default import Default
from sefazetllib.factory.platform.Platform import Platform


@Builder
class ExtractS3(Extract):
    warnings.warn(
        "The 'ExtractS3' class is deprecated. Please use the 'ExtractStorage' class with the protocol parameter (e.g., 's3a')."
    )
    platform: Platform = field(default=Default())
    file_format: str = field(default="")
    format_properties: Dict[str, Any] = field(default_factory=dict)
    repository: str = field(default="")
    layer: str = field(default="")
    schema: str = field(default="")
    entity: str = field(default="")
    url: str = field(default="")
    partition: List[str] = field(default_factory=list)
    etl_partition: bool = field(default=False)
    reference: str = field(default="")
    duplicates: bool = field(default=False)
    columns: List[str] = field(default_factory=list)
    optional: bool = field(default=False)
    partition_delimiter: str = field(default="/")

    def build_connection_string(self):
        self.url = f"s3a://{self.repository}/{self.layer}/{self.schema}/{self.entity}"

        if self.partition != []:
            try:
                partition = self.partition_delimiter.join(self.partition.get())
            except AttributeError:
                partition = self.partition_delimiter.join(self.partition)

            self.setUrl(f"{self.url}/{partition}")

        return self.url

    def execute(self, **kwargs):
        if isinstance(self.platform, Default):
            self.setPlatform(kwargs["platform"])

        local_repository = self.repository
        if local_repository == "":
            self.setRepository(kwargs["repository"])

        if self.etl_partition:
            self.setPartition(kwargs["partition"])

        if kwargs:
            args = kwargs["args"]
            if args.extractRepository and local_repository == "":
                self.setRepository(args.extractRepository)

            if args.extractPartitions:
                self.setPartition(args.extractPartitions)

            if args.extractUrl:
                url = args.extractUrl

        url = self.build_connection_string()

        return (
            self.reference,
            self.platform.read(
                file_format=self.file_format,
                format_properties=self.format_properties,
                url=url,
                duplicates=self.duplicates,
                columns=self.columns,
                optional=self.optional,
            ),
        )
