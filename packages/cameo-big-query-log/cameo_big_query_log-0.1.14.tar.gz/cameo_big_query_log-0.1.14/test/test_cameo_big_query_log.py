import pytest
from pytest_mock import mocker
from cameo_big_query_log.cameo_big_query_log import BigQueryLogger, UserData
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from cryptography.fernet import Fernet
import os
import datetime
import platform

# Mock environment variables
os.environ['BIG_QUERY_KEY'] = Fernet.generate_key().decode()
os.environ['BIG_QUREY_GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
os.environ['BIG_QUREY_DATASET_ID'] = 'test_dataset'
os.environ['BIG_QUREY_TABLE_NAME'] = 'test_table'

@pytest.fixture
def bigquery_logger():
    return BigQueryLogger()

def test_generate_key():
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

def test_insert_data_to_table(bigquery_logger, mocker):
    mocker.patch.object(bigquery.Client, 'from_service_account_json')
    mocker.patch.object(bigquery.Client, 'get_table', side_effect=NotFound('Table not found'))
    mocker.patch.object(bigquery.Client, 'create_table')
    mocker.patch.object(bigquery.Client, 'insert_rows_json', return_value=[])

    user_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": '{"message": "test"}'
    }

    bigquery_logger.insert_data_to_table(user_data)
    bigquery.Client.from_service_account_json.assert_called_once()
    bigquery.Client.get_table.assert_called_once()
    bigquery.Client.create_table.assert_called_once()
    bigquery.Client.insert_rows_json.assert_called_once()

def test_caculate_character_count():
    user_data = {
        "user_name": "test_user",
        "user_department": "test_department",
        "action_type": "login",
        "action_details": '{"message": "這是一個範例\\u6587\\u5b57, with 中英文混合 characters and punctuation!"}'
    }
    bigquery_logger = BigQueryLogger()
    total_count, count_chinese_count, count_english_count = bigquery_logger.caculate_character_count(user_data)
    assert total_count == 61
    assert count_chinese_count == 13
    assert count_english_count == 48
