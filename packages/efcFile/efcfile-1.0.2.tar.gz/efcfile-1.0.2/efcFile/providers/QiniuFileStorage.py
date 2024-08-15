import qiniu
import mimetypes
from typing import Any, List

import requests

from ..interfaces.FileStorageInterface import FileStorageInterface


class QiniuFileStorage(FileStorageInterface):
    def __init__(self, access_key: str, secret_key: str, bucket_name: str, domain: str, path_prefix: str = ''):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.domain = domain
        self.q = qiniu.Auth(access_key, secret_key)
        self.bucket = qiniu.BucketManager(self.q)
        self.path_prefix = path_prefix

    def put(self, key: str, data: Any) -> bool:
        try:
            token = self.q.upload_token(self.bucket_name, self.path_prefix + key)
            ret, info = qiniu.put_data(token, self.path_prefix + key, data)
            if info.status_code == 200:
                print(f"文件 '{key}' 已成功上传到 '{self.bucket_name}'。")
                return True
            else:
                print(f"上传失败：{info}")
        except Exception as e:
            print(f"上传异常：{e}")
        return False

    def get(self, key: str) -> bytes:
        try:
            url = self.domain + '/' + key
            ret, info = self.bucket.stat(self.bucket_name, self.path_prefix + key)
            if info.status_code == 200:
                private_url = self.q.private_download_url(url)
                response = requests.get(private_url)
                return response.content
            else:
                print(f"获取文件失败：{info}")
        except Exception as e:
            print(f"下载异常：{e}")
        return b''

    def delete(self, key: str) -> bool:
        try:
            ret, info = self.bucket.delete(self.bucket_name, self.path_prefix + key)
            if info.status_code == 200:
                print(f"文件 '{key}' 已成功删除。")
                return True
            else:
                print(f"删除失败：{info}")
        except Exception as e:
            print(f"删除异常：{e}")
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
            ret, info = self.bucket.copy(self.bucket_name, self.path_prefix + key, self.bucket_name,
                                         self.path_prefix + to_key)
            if info.status_code == 200:
                print(f"文件 '{key}' 已成功复制到 '{to_key}'。")
                return True
            else:
                print(f"复制失败：{info}")
        except Exception as e:
            print(f"复制异常：{e}")
        return False

    def exists(self, key: str) -> bool:
        try:
            ret, info = self.bucket.stat(self.bucket_name, self.path_prefix + key)
            return info.status_code == 200
        except Exception:
            return False

    def size(self, key: str) -> int:
        try:
            ret, info = self.bucket.stat(self.bucket_name, self.path_prefix + key)
            if info.status_code == 200:
                return ret['fsize']
            else:
                print(f"获取文件大小失败：{info}")
        except Exception as e:
            print(f"获取文件大小异常：{e}")
        return 0

    def list(self, key: str) -> List[str]:
        try:
            ret, eof, info = self.bucket.list(self.bucket_name, prefix=self.path_prefix + key)
            if info.status_code == 200 and 'items' in ret:
                files = [item['key'] for item in ret['items']]
                return files
            else:
                print(f"列出文件失败：{info}")
                return []
        except Exception as e:
            print(f"列出文件异常：{e}")
            return []

    def mime_type(self, key: str) -> str:
        try:
            ret, info = self.bucket.stat(self.bucket_name, self.path_prefix + key)
            if info.status_code == 200:
                mime_type = ret.get('mimeType')
                return mime_type or mimetypes.guess_type(key)[0] or "application/octet-stream"
            else:
                print(f"获取文件 MIME 类型失败：{info}")
        except Exception as e:
            print(f"获取文件 MIME 类型异常：{e}")
        return "application/octet-stream"
