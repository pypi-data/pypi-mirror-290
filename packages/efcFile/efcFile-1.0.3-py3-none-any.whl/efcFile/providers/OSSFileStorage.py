import oss2
import mimetypes
from typing import Any, List
from ..interfaces.FileStorageInterface import FileStorageInterface


class OSSFileStorage(FileStorageInterface):
    def __init__(self, access_key: str, secret_key: str, endpoint: str, bucket_name: str, path_prefix: str = ''):
        self.auth = oss2.Auth(access_key, secret_key)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        self.path_prefix = path_prefix

    def put(self, key: str, data: Any) -> bool:
        try:
            result = self.bucket.put_object(self.path_prefix + key, data)
            if result.status == 200:
                print(f"文件 '{key}' 已成功上传到 '{self.bucket.bucket_name}'。")
                return True
            else:
                print(f"上传失败，状态码：{result.status}")
        except oss2.exceptions.OssError as e:
            print(f"上传失败：{e}")
        return False

    def get(self, key: str) -> bytes:
        try:
            result = self.bucket.get_object(self.path_prefix + key)
            if result.status == 200:
                return result.read()
            else:
                print(f"下载失败，状态码：{result.status}")
        except oss2.exceptions.OssError as e:
            print(f"下载失败：{e}")
        return b''

    def delete(self, key: str) -> bool:
        try:
            result = self.bucket.delete_object(self.path_prefix + key)
            if result.status == 204:
                print(f"文件 '{key}' 已成功删除。")
                return True
            else:
                print(f"删除失败，状态码：{result.status}")
        except oss2.exceptions.OssError as e:
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
            result = self.bucket.copy_object(self.bucket.bucket_name, self.path_prefix + key, self.path_prefix + to_key)
            if result.status == 200:
                print(f"文件 '{key}' 已成功复制到 '{to_key}'。")
                return True
            else:
                print(f"复制失败，状态码：{result.status}")
        except oss2.exceptions.OssError as e:
            print(f"复制失败：{e}")
        return False

    def exists(self, key: str) -> bool:
        try:
            exists = self.bucket.object_exists(self.path_prefix + key)
            return exists
        except oss2.exceptions.OssError as e:
            print(f"检查文件是否存在失败：{e}")
        return False

    def size(self, key: str) -> int:
        try:
            result = self.bucket.get_object_meta(self.path_prefix + key)
            if result.status == 200:
                return result.content_length
            else:
                print(f"获取文件大小失败，状态码：{result.status}")
        except oss2.exceptions.OssError as e:
            print(f"获取文件大小失败：{e}")
        return 0

    def list(self, key: str) -> List[str]:
        try:
            files = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=self.path_prefix + key):
                files.append(obj.key)
            return files
        except oss2.exceptions.OssError as e:
            print(f"列出文件失败：{e}")
        return []

    def mime_type(self, key: str) -> str:
        try:
            result = self.bucket.get_object_meta(self.path_prefix + key)
            if result.status == 200:
                # 从 headers 中获取 Content-Type
                content_type = result.headers.get('Content-Type')
                return content_type or mimetypes.guess_type(key)[0] or "application/octet-stream"
            else:
                print(f"获取文件 MIME 类型失败，状态码：{result.status}")
        except oss2.exceptions.OssError as e:
            print(f"获取文件 MIME 类型失败：{e}")
        return "application/octet-stream"
