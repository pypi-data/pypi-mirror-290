from logging import Logger
from typing import Any, Callable
import requests
from urllib.parse import urljoin

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from pyeqx.core.models.module.properties import (
    ApiDataModuleProperties,
)
from pyeqx.core.models.storage.properties import (
    ApiDataProperties,
    CassandraDataProperties,
    MongoDataProperties,
    MSSqlDataProperties,
    PostgreSqlDataProperties,
    SqlDataProperties,
)
from pyeqx.core.spark.common import create_dataframe


class OperationReader:
    def __init__(self, spark_session: SparkSession, logger: Logger) -> None:
        self.__logger = logger
        self.__spark_session = spark_session

    def read_from_api(
        self,
        data_props: ApiDataModuleProperties,
        storage_props: ApiDataProperties,
        schema: StructType = None,
        success_handler: Callable[..., Any] = None,
        error_handler: Callable[..., Any] = None,
    ):
        response = self.__request_api(
            self.__build_request_api_options(
                data_props=data_props, storage_props=storage_props
            )
        )
        if response.status_code == 200:
            datas = (
                response.json()
                if success_handler is None
                else success_handler(response.json())
            )

            return create_dataframe(
                spark=self.__spark_session, schema=schema, datas=datas
            )
        else:
            if error_handler:
                error_handler(response.json())

    def read_from_mongodb(
        self,
        table: str,
        storage_props: MongoDataProperties,
        schema: StructType = None,
        options: dict = None,
    ) -> DataFrame:
        if options is None:
            options = {}

        spark_options = {
            "spark.mongodb.connection.uri": storage_props.uri,
            "spark.mongodb.database": storage_props.db,
            "spark.mongodb.collection": table,
        }

        options.update(spark_options)

        return self.read_from(
            schema=schema, format="mongodb", options=options, path=table
        )

    def read_from_cassandra(
        self,
        table: str,
        storage_props: CassandraDataProperties,
        options: dict = None,
    ):
        if options is None:
            options = {}

        spark_options = {
            "keyspace": storage_props.keyspace,
            "table": table,
        }

        options.update(spark_options)

        return self.read_from(
            schema=None,
            format="org.apache.spark.sql.cassandra",
            options=options,
            path=table,
        )

    def read_from_mssql(
        self,
        table: str,
        storage_props: MSSqlDataProperties,
        schema: StructType = None,
        options: dict = None,
    ) -> DataFrame:
        if options is None:
            options = {}

        spark_options = {
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        }

        options.update(spark_options)

        return self.read_from_sql(
            schema=schema,
            table=table,
            format="com.microsoft.sqlserver.jdbc.spark",
            storage_props=storage_props,
            options=options,
        )

    def read_from_postgresql(
        self,
        table: str,
        storage_props: PostgreSqlDataProperties,
        schema: StructType = None,
        options: dict = None,
    ) -> DataFrame:
        if options is None:
            options = {}

        spark_options = {
            "driver": "org.postgresql.Driver",
        }

        options.update(spark_options)

        return self.read_from_sql(
            schema=schema,
            table=table,
            storage_props=storage_props,
            options=options,
        )

    def read_from_sql(
        self,
        table: str,
        storage_props: SqlDataProperties,
        schema: StructType = None,
        format: str = "jdbc",
        options: dict = None,
    ) -> DataFrame:
        if options is None:
            options = {}

        spark_options = {
            "url": storage_props.url,
            "dbtable": table,
        }

        options.update(spark_options)

        return self.read_from(schema=schema, format=format, options=options, path=table)

    def read_from_s3(
        self,
        path: str,
        format: str,
        schema: StructType = None,
        options: dict = {},
    ) -> DataFrame:
        if options is None:
            options = {}

        return self.read_from(schema=schema, path=path, format=format, options=options)

    def read_from(
        self,
        format: str,
        schema: StructType = None,
        path: str = None,
        options: dict = {},
    ) -> DataFrame:
        if options is None:
            options = {}

        self.__logger.debug(f"reading data from type: {format}, table: {path}")

        reader = self.__spark_session.read.options(**options)

        if schema is not None:
            reader.schema(schema)

        if format == "csv":
            return reader.csv(path=path)
        elif format == "delta":
            return reader.format(format).load(path=path)
        else:
            return reader.format(format).load()

    def __build_request_api_options(
        self, data_props: ApiDataModuleProperties, storage_props: ApiDataProperties
    ) -> dict:
        options = {}
        headers = storage_props.headers
        method = str.lower(data_props.method)

        options["url"] = urljoin(
            storage_props.endpoint, storage_props.path + "/" + data_props.path
        )
        options["method"] = method
        options["parameters"] = data_props.parameters

        if not method:
            method = "get"

        if method == "post":
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"

            options["body"] = data_props.body

        options["headers"] = headers

        return options

    def __request_api(self, options: dict):
        url = options["url"]
        headers = options["headers"]
        method = options["method"]
        parameters = options["parameters"]

        if not method:
            method = "get"

        if method == "get":
            return requests.get(url, headers=headers, params=parameters)
        elif method == "post":
            body = options["body"]

            return requests.post(url, headers=headers, params=parameters, json=body)
