from google.cloud import bigquery
import datetime
import json
import socket
import platform
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import logging

# 設置日誌記錄
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加載 .env 文件中的環境變數
load_dotenv()

# 從環境變數中讀取密鑰
key = os.getenv('BIG_QUREY_KEY').encode()
cipher_suite = Fernet(key)
from google.api_core.exceptions import NotFound
from pydantic import BaseModel, Field, constr, model_validator, ValidationError

class UserData(BaseModel):
    user_name: str  # 必填
    user_department: str  # 必填
    domain_name: str = Field(default='unknown')  # 選填, default='unknown'
    session_id: str = Field(default='unknown')  # 選填, 對話的session_id, default='unknown'
    action_type: constr(min_length=1)  # 必填, 選項有login、logout、conversation、picture、video
    action_details: str  # 必填, log的詳細資訊, 字串形式, 如果是用completion, 可以直接json.dumps(messages)
    source_ip: str = Field(default='0.0.0.0')
    user_agent: str = Field(default='unknown')
    resource_id: str = Field(default='unknown')  # 選填, 可為波通鑒資料庫id、詢問的音檔或圖檔名稱 
    developer: str = Field(default='cameo')  # 選填, 開發者姓名, 預設cameo

    @model_validator(mode='after')
    def check_required_fields(cls, values):
        required_fields = ['user_name', 'user_department', 'action_type', 'action_details']
        missing_fields = [field for field in required_fields if not getattr(values, field, None)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        # 檢查 action_details 是否為有效的 JSON 字符串
        if not isinstance(values.action_details, str):
            raise ValueError("action_details 必須是有效的 JSON 字符串")
        return values

class BigQueryLogger:
    def __init__(self):
        self.key_path = os.getenv('BIG_QUREY_GOOGLE_APPLICATION_CREDENTIALS')
        self.client = bigquery.Client.from_service_account_json(self.key_path)
        self.cipher_suite = Fernet(key)

    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        return key.decode()

    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return '0.0.0.0'
        finally:
            s.close()

    def insert_data_to_table(self, user_data: dict):
        try:
            user_data = UserData(**user_data)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return

        try:
            user_ip = self.get_local_ip()
            user_agent = platform.platform()

            data = [{
                'timestamp': datetime.datetime.now().isoformat(),
                'user_name': user_data.user_name,
                'user_department': user_data.user_department,
                'domain_name': user_data.domain_name,
                'session_id': user_data.session_id,
                'action_type': user_data.action_type,
                'action_details': self.cipher_suite.encrypt(user_data.action_details.encode()).decode(),
                'source_ip': user_ip,
                'user_agent': user_agent,
                'resource_id': user_data.resource_id,
                'developer': user_data.developer
            }]

            dataset_id = os.getenv('BIG_QUREY_DATASET_ID')
            table_name = os.getenv('BIG_QUREY_TABLE_NAME')
            table_id = f'{self.client.project}.{dataset_id}.{table_name}'

            try:
                self.client.get_table(table_id)
                print(f"Table {table_id} already exists.")
            except NotFound:
                self.create_table(table_id)

            errors = self.client.insert_rows_json(table_id, data)
            if errors:
                print(f"Errors occurred while inserting rows: {errors}")
                return
            print(f"成功上傳資料到 {dataset_id}.{table_id}")
        except Exception as e:
            print(f"An error occurred: {e}")
        except ValidationError as e:
            logger.error(f"Validation error: {e}")

    def create_table(self, table_id):
        dataset_id = os.getenv('BIG_QUREY_TABLE_NAME')
        # table_id 已經是完整的格式

        schema = [
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED", description="時間"),
            bigquery.SchemaField("user_name", "STRING", description="使用者名稱"),
            bigquery.SchemaField("user_department", "STRING", description="使用者部門"),
            bigquery.SchemaField("domain_name", "STRING"),
            bigquery.SchemaField("session_id", "STRING", description="會話的唯一標識"),
            bigquery.SchemaField("action_type", "STRING", mode="REQUIRED", description="動作類型（如登入、登出、交談、上傳、下載等）"),
            bigquery.SchemaField("action_details", "STRING", mode="REQUIRED", description="動作詳細參數，以加密後的字符串存儲"),
            bigquery.SchemaField("source_ip", "STRING", mode="REQUIRED", description="使用者的IP地址"),
            bigquery.SchemaField("user_agent", "STRING", mode="REQUIRED", description="使用者的瀏覽器或客戶端信息"),
            bigquery.SchemaField("resource_id", "STRING", description="資源的唯一標識（如文件ID）"),
            bigquery.SchemaField("developer", "STRING", mode="REQUIRED", description="開發者名稱")
        ]

        time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="timestamp"
        )

        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = time_partitioning
        table = self.client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id} with daily partitioning")

