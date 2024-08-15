"""
# 申请access_key和secret_key教程 https://developers.cloudflare.com/r2/api/s3/tokens/
storage = S3FileStorage(
    access_key='access_key',
    secret_key='secret_key',
    endpoint_url='https://xx.r2.cloudflarestorage.com',
    bucket_name='xx',
    path_prefix='xxx/'
)
"""
import boto3
import mimetypes
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Any, List
from ..interfaces.FileStorageInterface import FileStorageInterface


class S3FileStorage(FileStorageInterface):
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, region_name: str = 'auto',
                 bucket_name: str = '', path_prefix: str = ''):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name
        )
        self.bucket_name = bucket_name
        self.path_prefix = path_prefix

    def put(self, key: str, data: Any) -> bool:
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=self.path_prefix + key, Body=data)
            print(f"文件 '{key}' 已成功上传到 '{self.bucket_name}'。")
            return True
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"上传失败：{e}")

        return False

    def get(self, key: str) -> bytes:
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.path_prefix + key)
            return response['Body'].read()
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"下载失败：{e}")
            return b''

    def delete(self, key: str) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.path_prefix + key)
            print(f"文件 '{key}' 已成功删除。")
            return True
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"删除失败：{e}")
        return False

    def move(self, key: str, to_key: str) -> bool:
        try:
            self.copy(key, to_key)
            self.delete(key)
            return True
        except Exception as e:
            print(f"移动失败：{e}")
            return False

    def copy(self, key: str, to_key: str) -> bool:
        try:
            copy_source = {'Bucket': self.bucket_name, 'Key': self.path_prefix + key}
            self.s3_client.copy_object(CopySource=copy_source, Bucket=self.bucket_name, Key=to_key)
            print(f"文件 '{key}' 已成功复制到 '{to_key}'。")
            return True
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"复制失败：{e}")
            return False

    def exists(self, key: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=self.path_prefix + key)
            return True
        except ClientError:
            return False

    def size(self, key: str) -> int:
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=self.path_prefix + key)
            return response['ContentLength']
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"获取文件大小失败：{e}")
            return 0

    def list(self, key: str) -> List[str]:
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.path_prefix + key)
            if 'Contents' in response:
                files = [item['Key'] for item in response['Contents']]
                return files
            else:
                return []
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"列出文件失败：{e}")
            return []

    def mime_type(self, key: str) -> str:
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=self.path_prefix + key)
            # 检查 'ContentType' 是否存在于响应中
            content_type = response.get('ContentType')
            return content_type or mimetypes.guess_type(key)[0] or "application/octet-stream"
        except NoCredentialsError:
            print("凭证错误：无法找到 AWS 凭证。")
        except ClientError as e:
            print(f"获取文件 MIME 类型失败：{e}")
        return "application/octet-stream"
