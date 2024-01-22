import logging
import os

import pytest
import copy
from conftest import (initialize_tests,
                      create_and_fill_table,
                      create_bucket_clear_directory,
                      create_view,
                      check_number_and_sum,
                      TABLE_NAME)
from clickhouse_s3_etl_tools.s3_exporter.s3_exporter import export_to_s3
from clickhouse_s3_etl_tools.s3_to_clickhouse_transfer.s3_to_clickhouse_transfer import transfer_s3_to_clickhouse
from clickhouse_s3_etl_tools.schema.schema_configs import Configuration
from clickhouse_s3_etl_tools.connectors.s3_connector import S3Connector
from clickhouse_s3_etl_tools.connectors.clickhouse_connector import ClickHouseConnector


@pytest.mark.parametrize(
    "create_and_fill_table, create_bucket_clear_directory",
    [
        pytest.param(None, None, marks=pytest.mark.dependency(name="test_export_common"))
    ],
    indirect=["create_and_fill_table", "create_bucket_clear_directory"]
)
def test_export(create_and_fill_table, create_bucket_clear_directory, initialize_tests):
    export_to_s3(initialize_tests)


@pytest.mark.parametrize(
    "create_and_fill_table, create_bucket_clear_directory",
    [
        pytest.param("test_by_part", "test_by_part", marks=pytest.mark.dependency(name="test_export_by_part"))
    ],
    indirect=["create_and_fill_table", "create_bucket_clear_directory"]
)
def test_export_by_not_part_field(initialize_tests, create_and_fill_table, create_bucket_clear_directory):
    config: Configuration = copy.deepcopy(initialize_tests)
    config.table.TABLE_NAME = "test_by_part"
    config.PARTITION_KEY = "column2"
    export_to_s3(config)


@pytest.mark.parametrize("create_view", ["_view_suffix"], indirect=True)
@pytest.mark.parametrize("create_bucket_clear_directory", [f"{TABLE_NAME}_view_suffix"], indirect=True)
def test_export_view(initialize_tests, create_view, create_bucket_clear_directory):
    config_: Configuration = copy.deepcopy(initialize_tests)
    config_.table.TABLE_NAME = config_.table.TABLE_NAME + "_view_suffix"
    export_to_s3(config_)
    # only metadata exists
    with S3Connector(config_.s3) as s3_conn:
        s3_path_folder: str = f"{config_.table.DATABASE}/{config_.table.TABLE_NAME}"
        meta_path: str = f"{s3_path_folder}/__metadata__{config_.table.TABLE_NAME}.parquet"
        file_list = s3_conn.get_file_list(s3_path_folder)
        assert meta_path in file_list, f"No {meta_path} in s3 folder for metadata"
        assert len(file_list) == 1, f"Only {meta_path} should be in folder for {config_.table.TABLE_NAME}"


@pytest.mark.dependency(depends=["test_export_common"])
def test_transfer(initialize_tests):
    config = initialize_tests
    transfer_s3_to_clickhouse(initialize_tests)
    check_number_and_sum(config)


@pytest.mark.dependency(depends=["test_export_by_part"])
def test_transfer_by_part(initialize_tests):
    config: Configuration = copy.deepcopy(initialize_tests)
    config.table.TABLE_NAME = "test_by_part"
    transfer_s3_to_clickhouse(config)
    check_number_and_sum(config)
