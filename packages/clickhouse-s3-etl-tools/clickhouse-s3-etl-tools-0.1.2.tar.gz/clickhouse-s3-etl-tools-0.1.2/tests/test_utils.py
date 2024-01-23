import logging
from dotenv import load_dotenv
from clickhouse_s3_etl_tools.utils import update_create_table_query
from clickhouse_s3_etl_tools.configs.config_module import get_configuration
from clickhouse_s3_etl_tools.schema.schema_configs import Configuration

load_dotenv(".env-test")


def test_update_create_table_query_collapsed():
    config: Configuration = get_configuration()
    ddl_test = """CREATE TABLE test.table1 (`column1` Int64) ENGINE = ReplicatedCollapsingMergeTree('path', '{replica}', Sign)"""
    config.table.TABLE_NAME = 'table1'
    config.table.DATABASE = 'test'
    assert update_create_table_query(ddl_test, config) == """CREATE TABLE test2.table1  (`column1` Int64) ENGINE = ReplicatedCollapsingMergeTree(Sign)"""
