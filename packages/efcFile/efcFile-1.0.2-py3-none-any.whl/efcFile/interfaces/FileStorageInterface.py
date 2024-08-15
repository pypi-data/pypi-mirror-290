from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class FileStorageInterface(ABC):
    @abstractmethod
    def put(self, key: str, data: Any) -> bool:
        """保存文件"""
        pass

    @abstractmethod
    def get(self, key: str) -> bytes:
        """获取文件"""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除文件"""
        pass

    @abstractmethod
    def move(self, key: str, to_key: str) -> bool:
        """移动文件"""
        pass

    @abstractmethod
    def copy(self, key: str, to_key: str) -> bool:
        """复制文件"""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """文件是否存在"""
        pass

    @abstractmethod
    def size(self, key: str) -> int:
        """文件大小"""
        pass

    @abstractmethod
    def list(self, key: str) -> List[str]:
        """文件列表"""
        pass

    @abstractmethod
    def mime_type(self, key: str) -> str:
        """获取文件的MIME类型"""
        pass
