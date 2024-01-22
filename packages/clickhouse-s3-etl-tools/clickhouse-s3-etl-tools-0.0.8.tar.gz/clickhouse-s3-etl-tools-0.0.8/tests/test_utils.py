import re

# Sample input string
create_table_query = """
REATE TABLE test.table1
(
    `column1`       Int64
) ENGINE = ReplicatedCollapsingMergeTree('path', '{replica}',sign) PARTITION BY tuple() ORDER BY id SETTINGS index_granularity = 8192
"""

# Define the regular expression pattern
pattern = r"CollapsingMergeTree\((.*?)\s*(?:,\s*[^,\n]+\s*)*?,\s*([^,\n]+)\s*\)"

# Perform the substitution
create_table_query = re.sub(
    pattern=pattern,
    repl=r"CollapsingMergeTree(\2)",
    string=create_table_query,
    flags=re.DOTALL,  # Use DOTALL to match across new lines
)

print(create_table_query)

# import logging
# from dotenv import load_dotenv
# from clickhouse_s3_etl_tools.utils import update_create_table_query
# from clickhouse_s3_etl_tools.configs.config_module import get_configuration
# from clickhouse_s3_etl_tools.schema.schema_configs import Configuration
#
# load_dotenv(".env-test")
#
#
# def update_create_table_query_collapsed():
#     config: Configuration = get_configuration()
#     ddl_test = """CREATE TABLE test.table1
# (
#     `column1`       Int64
# ) ENGINE = ReplicatedCollapsingMergeTree('path', '{replica}',
#                                          Sign) PARTITION BY tuple() ORDER BY id SETTINGS index_granularity = 8192"""
#     config.table.TABLE_NAME = 'table1'
#     config.table.DATABASE = 'test'
#     assert update_create_table_query(ddl_test, config) == """CREATE TABLE test2.table1
# (
#     `column1`       Int64
# ) ENGINE = ReplicatedCollapsingMergeTree(Sign) PARTITION BY tuple() ORDER BY id SETTINGS index_granularity = 8192
# """
#
#
#
# update_create_table_query_collapsed()
