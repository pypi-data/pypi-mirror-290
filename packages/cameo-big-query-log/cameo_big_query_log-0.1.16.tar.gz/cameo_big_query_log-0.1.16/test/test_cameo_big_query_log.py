import pytest
from unittest.mock import MagicMock
from cameo_big_query_log.cameo_big_query_log import BigQueryLogger, UserData
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from cryptography.fernet import Fernet
import os

# Mock environment variables
os.environ['BIG_QUERY_KEY'] = Fernet.generate_key().decode()
os.environ['BIG_QUERY_GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/apple/Downloads/scoop-386004-e9c7b6084fb4.json'
os.environ['BIG_QUERY_DATASET_ID'] = 'test_dataset'
os.environ['BIG_QUERY_TABLE_NAME'] = 'test_table'

@pytest.fixture
def bigquery_logger():
    return BigQueryLogger()

def test_insert_data_to_table(bigquery_logger, mocker):
    mock_client = mocker.patch.object(bigquery_logger, 'client')
    mock_client.insert_rows_json.return_value = []

    user_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": '{"message": "test"}'
    }
    bigquery_logger.insert_data_to_table(user_data)
    mock_client.insert_rows_json.assert_called_once()
    user_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": '{"message": "test"}'
    }
    bigquery_logger.insert_data_to_table(user_data)
    # 這裡可以添加更多的斷言來檢查數據是否正確插入

def test_check_and_add_columns(bigquery_logger, mocker):
    mock_client = mocker.patch.object(bigquery_logger, 'client')
    mock_client.get_table.return_value.schema = []

    table_id = f'{bigquery_logger.client.project}.{bigquery_logger.dataset_id}.{bigquery_logger.table_name}'
    data = {
        "new_field": "test_value"
    }
    bigquery_logger.check_and_add_columns(table_id, data)
    mock_client.update_table.assert_called_once()
    table_id = f'{bigquery_logger.client.project}.{bigquery_logger.dataset_id}.{bigquery_logger.table_name}'
    data = {
        "new_field": "test_value"
    }
    bigquery_logger.check_and_add_columns(table_id, data)
    # 這裡可以添加更多的斷言來檢查欄位是否正確添加

def test_create_table(bigquery_logger, mocker):
    mock_client = mocker.patch.object(bigquery_logger, 'client')
    mock_table = MagicMock()
    mock_table.project = "test_project"
    mock_table.dataset_id = "test_dataset"
    mock_table.table_id = "new_test_table"
    mock_client.create_table.return_value = mock_table
    mock_client.project = "test_project"

    table_id = f'{bigquery_logger.client.project}.{bigquery_logger.dataset_id}.new_test_table'
    bigquery_logger.create_table(table_id)
    mock_client.create_table.assert_called_once()
    table_id = f'{bigquery_logger.client.project}.{bigquery_logger.dataset_id}.new_test_table'
    bigquery_logger.create_table(table_id)
    # 這裡可以添加更多的斷言來檢查表是否正確創建

def test_create_dataset_if_not_exists(bigquery_logger, mocker):
    mock_client = mocker.patch.object(bigquery_logger, 'client')
    mock_client.get_dataset.side_effect = NotFound('Dataset not found')
    mock_client.create_dataset.return_value = None

    dataset_id = "new_test_dataset"
    bigquery_logger.create_dataset_if_not_exists(dataset_id)
    mock_client.create_dataset.assert_called_once()
    dataset_id = "new_test_dataset"
    bigquery_logger.create_dataset_if_not_exists(dataset_id)
    # 這裡可以添加更多的斷言來檢查數據集是否正確創建
    key = BigQueryLogger.generate_key()
    assert isinstance(key, str)
    assert len(key) > 0

def test_get_local_ip():
    ip = BigQueryLogger.get_local_ip()
    assert isinstance(ip, str)
    assert ip.count('.') == 3

def test_user_data_validation():
    valid_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": '{"message": "test"}'
    }
    user_data = UserData(**valid_data)
    assert user_data.user_name == "test_user"
    assert user_data.user_department == "test_department"

    invalid_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": 123  # Invalid type
    }
    with pytest.raises(ValueError):
        UserData(**invalid_data)

def test_caculate_character_count():
    user_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": '{"message": "這是一個範例\\u6587\\u5b57, with 中英文混合 characters and punctuation!"}'
    }
    bigquery_logger = BigQueryLogger()
    total_count, count_chinese_count, count_english_count = bigquery_logger.caculate_character_count(user_data)
    assert total_count == 63
    assert count_chinese_count == 13
    assert count_english_count == 50
