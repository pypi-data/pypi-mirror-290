# efcFIle

通用的文件储存类 支持本地、S3、OSS、Qiniu

```
pip install efcFile
```

```python

import efcFile
manager = efcFile.FileStorageManager(default_storage="local")
manager.set_storage("local", efcFile.LocalFileStorage(storage_path="./storage/"))
manager.put("example.txt", b"This is a test file")
print(manager.get("example.txt"))
print(manager.exists("example.txt"))
print(manager.size("example.txt"))
print(manager.mime_type("example.txt"))
print(manager.list(""))
manager.move("example.txt", "example_moved.txt")
print(manager.exists("example_moved.txt"))
manager.delete("example_moved.txt")

manager.set_storage("s3", efcFile.S3FileStorage(access_key="", secret_key="", endpoint_url="", region_name="auto", bucket_name=""))

manager.set_storage("oss", efcFile.OSSFileStorage(access_key="", secret_key="", endpoint="", bucket_name="", path_prefix=""))

manager.set_storage("qiniu", efcFile.QiniuFileStorage(access_key="", secret_key="", bucket_name="", domain="", path_prefix=""))

```

