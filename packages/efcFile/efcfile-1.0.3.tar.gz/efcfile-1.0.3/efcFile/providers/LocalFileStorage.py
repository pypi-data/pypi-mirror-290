import os
import shutil
import mimetypes
from typing import Any, List

from ..interfaces.FileStorageInterface import FileStorageInterface


class LocalFileStorage(FileStorageInterface):
    def __init__(self, storage_path: str = "./storage/"):
        self.storage_path = storage_path
        if not self.storage_path.endswith('/'):
            self.storage_path += '/'

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def put(self, key: str, data: Any) -> bool:
        with open(os.path.join(self.storage_path, key), 'wb') as f:
            f.write(data)
            return True
        return False

    def get(self, key: str) -> bytes:
        with open(os.path.join(self.storage_path, key), 'rb') as f:
            return f.read()


    def delete(self, key: str) -> bool:
        os.remove(os.path.join(self.storage_path, key))
        return True

    def move(self, key: str, to_key: str) -> bool:
        shutil.move(os.path.join(self.storage_path, key), os.path.join(self.storage_path, to_key))
        return True

    def copy(self, key: str, to_key: str) -> bool:
        shutil.copy2(os.path.join(self.storage_path, key), os.path.join(self.storage_path, to_key))
        return True

    def exists(self, key: str) -> bool:
        return os.path.exists(os.path.join(self.storage_path, key))

    def size(self, key: str) -> int:
        return os.path.getsize(os.path.join(self.storage_path, key))

    def list(self, key: str) -> List[str]:
        return [f for f in os.listdir(self.storage_path) if os.path.isfile(os.path.join(self.storage_path, f))]

    def mime_type(self, key: str) -> str:
        return mimetypes.guess_type(os.path.join(self.storage_path, key))[0] or "application/octet-stream"
