import re
import time

import sqlparse
from clickhouse_s3_etl_tools.logger import get_logger
from clickhouse_s3_etl_tools.schema.schema_configs import Configuration
from clickhouse_s3_etl_tools.exceptions.exception import RowsMismatchError

logger = get_logger(__name__)


def check_rows_mismatch(s3_row_count: int,
                        clickhouse_row_count: int,
                        max_percentage_diff: float,
                        is_export: bool = True) -> None:
    """
    Check if there is a mismatch in the number of rows between ClickHouse and S3.

    Parameters:
    - s3_row_count (int): The number of rows in S3.
    - clickhouse_row_count (int): The total number
    Raises:
   - RowsMismatchError: If the conditions for row mismatch are met.
    """

    row_difference: int = abs((s3_row_count - clickhouse_row_count))

    if s3_row_count == clickhouse_row_count:
        mismatch_percentage = 0
    elif is_export:
        mismatch_percentage = row_difference / s3_row_count * 100
    else:
        mismatch_percentage = row_difference / clickhouse_row_count * 100

    if is_export:
        is_mismatch: bool = s3_row_count < clickhouse_row_count
    else:
        is_mismatch: bool = s3_row_count > clickhouse_row_count

    if is_mismatch or mismatch_percentage > max_percentage_diff:
        raise RowsMismatchError(s3_row_count, clickhouse_row_count, max_percentage_diff)


def prettify_sql(sql_query):
    parsed = sqlparse.format(sql_query, reindent=True)
    return parsed


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(
            f"Execution started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
        )

        result = func(*args, **kwargs)

        end_time = time.time()
        logger.info(
            f"Execution finished at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"
        )

        execution_time = end_time - start_time
        hours, remainder = divmod(execution_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (execution_time - int(execution_time)) * 1000

        logger.info(
            f"Total execution time: {int(hours)}h {int(minutes)}m {int(seconds)}s {int(milliseconds)}ms"
        )

        return result

    return wrapper


def update_create_table_query(create_table_query: str, config: Configuration):
    create_table_query = create_table_query.replace(
        config.table.DATABASE + ".", config.table.DATABASE_DESTINATION + "."
    )

    if config.ON_CLUSTER_DIRECTIVE != "":
        create_table_query = create_table_query.replace(
            f"{config.table.DATABASE_DESTINATION}.{config.table.TABLE_NAME}",
            f"{config.table.DATABASE_DESTINATION}.{config.table.TABLE_NAME} {config.get_on_cluster()}",
        )

    create_table_query = re.sub(
        pattern=r"CollapsingMergeTree\((.*?)\s*(?:,\s*[^,\n]+\s*)*?,\s*([^,\n]+)\s*\)",
        repl=r"CollapsingMergeTree(\2)",
        string=create_table_query,
    )
    return re.sub(
        pattern=r"MergeTree\('.*?'\)", repl="MergeTree()", string=create_table_query
    )


def build_s3_path(config: Configuration, filename: str) -> str:
    return f"{config.s3.PATH_S3}/{config.table.DATABASE}/{config.table.TABLE_NAME}/{filename}"


def build_s3_source(config: Configuration, filename: str) -> str:
    """
    Build the S3 source path or S3 Cluster source based on the configuration.

    Args:
        config (Configuration): The configuration object.
        filename (str): The filename for the S3 source.

    Returns:
        str: The constructed S3 source path or S3 Cluster source.
    """
    s3_path = build_s3_path(config, filename)
    if config.USE_S3_CLUSTER:
        return f"""s3Cluster(
        '{config.ON_CLUSTER_DIRECTIVE}',
        '{s3_path}',
        '{config.s3.S3_ACCESS_KEY}',
        '{config.s3.S3_SECRET_KEY}',
        'Parquet'
    )"""
    return f"""s3(
        '{s3_path}',
        '{config.s3.S3_ACCESS_KEY}',
        '{config.s3.S3_SECRET_KEY}',
        'Parquet'
    )"""
