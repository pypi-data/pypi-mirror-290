from typing import Any, List

from ..interfaces.FileStorageInterface import FileStorageInterface


class FileStorageManager:
    def __init__(self, default_storage: str):
        self.storages = {}
        self.current_storage = default_storage

    def set_storage(self, storage_name: str, storage: FileStorageInterface):
        self.storages[storage_name] = storage
        return self

    def disk(self, storage_name: str) -> FileStorageInterface:
        if storage_name not in self.storages:
            raise ValueError("Storage not set")
        return self.storages[storage_name]

    def get_disk(self) -> FileStorageInterface:
        if self.current_storage not in self.storages:
            raise ValueError("Storage not set")
        return self.storages[self.current_storage]

    def put(self, key: str, data: Any) -> None:
        return self.get_disk().put(key, data)

    def get(self, key: str) -> bytes:
        return self.get_disk().get(key)

    def delete(self, key: str) -> None:
        return self.get_disk().delete(key)

    def move(self, key: str, to_key: str) -> bool:
        return self.get_disk().move(key, to_key)

    def copy(self, key: str, to_key: str) -> bool:
        return self.get_disk().copy(key, to_key)

    def exists(self, key: str) -> bool:
        return self.get_disk().exists(key)

    def size(self, key: str) -> int:
        return self.get_disk().size(key)

    def list(self, key: str) -> List[str]:
        return self.get_disk().list(key)

    def mime_type(self, key: str) -> str:
        return self.get_disk().mime_type(key)
