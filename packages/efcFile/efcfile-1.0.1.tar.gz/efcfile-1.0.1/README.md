# efcFIle

通用的文件储存类

```python
from efcFile import FileStorageManager, LocalFileStorage

manager = FileStorageManager(default_storage="local")
manager.set_storage("local", LocalFileStorage(storage_path="./storage/"))
manager.put("example.txt", b"This is a test file")
print(manager.get("example.txt"))
print(manager.exists("example.txt"))
print(manager.size("example.txt"))
print(manager.mime_type("example.txt"))
print(manager.list(""))
manager.move("example.txt", "example_moved.txt")
print(manager.exists("example_moved.txt"))
manager.delete("example_moved.txt")

```