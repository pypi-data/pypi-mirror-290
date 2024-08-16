from logging import Logger
from typing import Optional

from pyspark.sql import DataFrame

from pyeqx.core.common import SPARK_S3_PATH_PREFIX


class OperationWriter:
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger

    def write_to_s3(
        self, data: DataFrame, mode: str, path: str, options: Optional[dict]
    ) -> None:
        if options is None:
            options = {}

        path_prefix = SPARK_S3_PATH_PREFIX

        actual_options = {"mergeSchema": False}
        actual_path = f"{path_prefix}{path}"

        for key, value in actual_options.items():
            options[key] = value

        if actual_path != "":
            self.write_to(
                data=data, format="delta", mode=mode, path=actual_path, options=options
            )

    def write_to_mssql(
        self,
        data: DataFrame,
        mode: str,
        url: str,
        table: str,
        options: Optional[dict],
    ) -> None:
        if options is None:
            options = {}

        spark_options = {
            "url": url,
            "dbtable": table,
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "batchsize": 1048576,
            "schemaCheckEnabled": False,
            "tableLock": True,
        }

        options.update(spark_options)

        self.write_to_sql(
            data=data,
            mode=mode,
            format="com.microsoft.sqlserver.jdbc.spark",
            options=options,
        )

    def write_to_postgresql(
        self,
        data: DataFrame,
        mode: str,
        url: str,
        table: str,
        options: Optional[dict],
    ) -> None:
        if options is None:
            options = {}

        spark_options = {
            "url": url,
            "dbtable": table,
            "driver": "org.postgresql.Driver",
            "batchsize": 1048576,
            "schemaCheckEnabled": False,
            "tableLock": True,
        }

        options.update(spark_options)

        self.write_to_sql(
            data=data,
            mode=mode,
            options=options,
        )

    def write_to_sql(
        self,
        data: DataFrame,
        mode: str,
        format: str = "jdbc",
        options: dict = {},
    ) -> None:
        self.write_to(
            data=data,
            format=format,
            mode=mode,
            options=options,
        )

    def write_to_mongodb(
        self,
        data: DataFrame,
        mode: str,
        uri: str,
        db: str,
        table: str,
        options: Optional[dict],
    ) -> None:
        if options is None:
            options = {}

        spark_options = {
            "spark.mongodb.connection.uri": uri,
            "spark.mongodb.database": db,
            "spark.mongodb.collection": table,
        }

        options.update(spark_options)

        self.write_to(data=data, format="mongodb", mode=mode, options=options)

    def write_to(
        self,
        data: DataFrame,
        format: str,
        mode: str,
        path: str = None,
        options: dict = {},
    ) -> None:
        self.__logger.debug(
            f"writing data to format: {format}, mode: {mode}, path: {path}."
        )

        writer = data.write.options(**options)

        modes = ["append", "overwrite"]

        parsed_mode = mode.lower()
        actual_mode = parsed_mode if parsed_mode in modes else "append"

        writer.format(format).mode(actual_mode).save(path)
