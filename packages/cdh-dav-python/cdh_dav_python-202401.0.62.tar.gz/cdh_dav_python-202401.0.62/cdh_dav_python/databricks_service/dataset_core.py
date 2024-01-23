""" Module with a variety of utility function for Spark data frames. """

from collections import Counter

# libraries
from importlib import util

# util
import hashlib
import uuid
import os
import sys

# spark /data
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, udf, expr, coalesce
from pyspark.sql.types import StringType

uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    import pyspark.pandas as pd

    # bug - pyspark version will not read local files in the repo
    # import pandas as pd
else:
    import pandas as pd
import hashlib
from pyspark.sql import DataFrame
import hashlib


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

from cdh_dav_python.cdc_admin_service.environment_logging import LoggerSingleton


def encrypt_value(pii_col):
    """Encypts a value using Databricks encryption library.

    Args:
        pii_col (_type_): Column to encrypt.

    Returns:
        _type_: Encrypted value
    """
    sha_value = hashlib.sha1(pii_col.encode()).hexdigest()
    return sha_value


encrypt_value_udf = udf(encrypt_value, StringType())


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class DataSetCore:
    """Core class for Spark Datasets"""

    @classmethod
    def add_row_id_to_dataframe(
        cls,
        sorted_df: DataFrame,
        row_id_keys: str,
        yyyy_param: str,
        mm_param: str,
        dd_param: str,
        data_product_id: str,
        environment: str,
    ) -> DataFrame:
        """Adds row_id column to the dataframe, the row_id a required unique identifier used
        to perform incremental updates.

        - Replaces {yyyy}, {mm}, or {dd} with the current year, month, or day in row id template
        - Create row_id based on template
        - If row_id_key is empty, then uses uuid to create row_id

        Args:
            sorted_df (DataFrame): Dataframe to add column
            row_id_keys (str): Comma separated list of keys to use to generate row_id
            yyyy_param (str): Year parameter to use to generate row_id
            mm_param (str): Month parameter to use to generate row_id
            dd_param (str): Day parameter to use to generate row_id

        Returns:
            DataFrame: Dataframe with added row_id column
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("add_row_id_to_dataframe"):
            try:
                if row_id_keys is None:
                    row_id_keys = ""
                row_id_keys = row_id_keys.strip()
                row_id_keys_list = row_id_keys.split(",")
                if len(row_id_keys_list) > 0 and len(row_id_keys) > 0:
                    sql_expr = row_id_keys
                    sql_expr = sql_expr.replace("{yyyy}", yyyy_param)
                    sql_expr = sql_expr.replace("{mm}", mm_param)
                    sql_expr = sql_expr.replace("{dd}", dd_param)
                else:
                    sql_expr = "uuid()"
                sql_expr = "concat_ws('-'," + sql_expr + ")"
                logger.info(f"attempting to update deltalake: sql_expr: {sql_expr}")

                assert " " not in "".join(sorted_df.columns)
                results_df = sorted_df.withColumn("row_id", expr(sql_expr))

                return results_df
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def encrypt_value(pii_col, data_product_id: str, environment: str):
        """Encypts value to store in databricks column

        Args:
            pii_col (any): Value to encrypt

        Returns:
            any: Encrpyted value
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("encrypt_value"):
            try:
                sha_value = hashlib.sha1(pii_col.encode()).hexdigest()
                return sha_value
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def table_exists(
        spark,
        dataset_name: str,
        database_name: str,
        data_product_id: str,
        environment: str,
    ):
        """Verifies if a dataset exists in databricks

        Args:
            spark (_type_): spark object
            dataset_name (_type_): dataset name to check
            database_name (_type_): database name to check

        Returns:
            _type_:  True if dataset exists
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("table_exists"):
            try:
                datasets_list_df = spark.sql(f"SHOW TABLES from {database_name}")
                datasets_list_df = datasets_list_df.filter(
                    datasets_list_df.tableName == f"{dataset_name}"
                )
                return datasets_list_df.count() > 0
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def scrub_object_name(
        original_object_name: str, data_product_id: str, environment: str
    ) -> str:
        """Scrubs characters in object to rename

        Args:
            original_object_name (str): original column name

        Returns:
            str: new object name
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("scrub_object_name"):
            try:
                if original_object_name is None:
                    original_object_name = "object_name_is_missing"

                c_renamed = original_object_name
                c_renamed = c_renamed.replace("†", "_")
                c_renamed = c_renamed.replace(",", "_")
                c_renamed = c_renamed.replace("*", "_")
                c_renamed = c_renamed.replace(" ", "_")
                c_renamed = c_renamed.replace("\r", "_")
                c_renamed = c_renamed.replace("\n", "_")
                c_renamed = c_renamed.replace(";", "")
                c_renamed = c_renamed.replace(".", "")
                c_renamed = c_renamed.replace("}", "")
                c_renamed = c_renamed.replace("{", "")
                c_renamed = c_renamed.replace("(", "")
                c_renamed = c_renamed.replace(")", "")
                c_renamed = c_renamed.replace("?", "")
                c_renamed = c_renamed.replace("-", "")
                c_renamed = c_renamed.replace("/", "")
                c_renamed = c_renamed.replace("//", "")
                c_renamed = c_renamed.replace("=", "_")
                c_renamed = c_renamed.replace("&", "w")
                c_renamed = c_renamed.lower()
                c_renamed = c_renamed.strip()

                return c_renamed
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def rename_column_names_as_unique(
        original_list, data_product_id: str, environment: str
    ):
        """Make all the items unique by adding a suffix (1, 2, etc).

        `seq` is mutable sequence of strings.
        `suffs` is an optional alternative suffix iterable.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("rename_column_names_as_unique"):
            try:
                new_list = []
                for i, original_col in enumerate(original_list):
                    if original_col is None:
                        original_col = "Column"
                        resulted_counter = Counter(
                            original_list
                        )  # {'foo': 2, 'bar': 1, None: 2}
                        totalcount = resulted_counter[None]  # 2
                        count = original_list[:i].count(None)
                    elif original_col == "":
                        original_col = "Column"
                        resulted_counter = Counter(
                            original_list
                        )  # {'foo': 2, 'bar': 1, None: 2}
                        totalcount = resulted_counter[""]  # 2
                        count = original_list[:i].count("")
                    else:
                        totalcount = original_list.count(original_col)
                        count = original_list[:i].count(original_col)

                    if totalcount > 1:
                        new_name = original_col + str(count + 1)
                    else:
                        new_name = original_col

                    new_list.append(new_name)
                return new_list
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def database_object_exists(
        spark, database_name, data_product_id: str, environment: str, dataset_name=None
    ):
        """Verifies if a dataset exists in databricks

        Args:
            spark (_type_): spark object
            dataset_name (_type_): dataset name to check
            database_name (_type_): database name to check

        Returns:
            _type_:  True if dataset exists
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("database_object_exists"):
            try:
                datasets_list_df = spark.sql(f"SHOW TABLES from {database_name}")

                if dataset_name is not None:
                    datasets_list_df = datasets_list_df.filter(
                        datasets_list_df.tableName == f"{dataset_name}"
                    )

                dataset_name = str(dataset_name)

                if datasets_list_df.first() is not None:
                    logger.info(f"Database Object {dataset_name} found")
                    return True
                else:
                    logger.warning(f"Dataset Object {dataset_name} not found")
                    return False
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def encrpyt_pii_columns(
        cls,
        pii_columns: str,
        is_using_standard_column_names: str,
        sorted_df: DataFrame,
        data_product_id: str,
        environment: str,
    ) -> DataFrame:
        """Encrypts the columns that are marked as PII

        Args:
            pii_columns (str): Comma delimited list of PII columns
            is_using_standard_column_names (str): Either None or "force_lowercase"
            sorted_df (DataFrame): Dataframe to be encrypted

        Returns:
            DataFrame: Encrypted dataframe
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("encrpyt_pii_columns"):
            try:
                logger.info(f"pii_columns:{pii_columns}")
                if pii_columns is not None:
                    pii_columns_list = pii_columns.split(",")
                    for col_orig in pii_columns_list:
                        if is_using_standard_column_names == "force_lowercase":
                            col_orig = col_orig.lower()
                            col_orig = col_orig.replace("'", "")
                            col_orig = col_orig.replace('"', "")
                        sorted_df = sorted_df.withColumn(
                            col_orig, coalesce(col_orig, lit("null"))
                        ).withColumn(col_orig, encrypt_value_udf(col_orig))

                return sorted_df
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
