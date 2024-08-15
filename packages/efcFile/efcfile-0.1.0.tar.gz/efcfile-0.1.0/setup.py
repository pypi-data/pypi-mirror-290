from setuptools import setup, find_packages

setup(
    name='efcFile',  # 包名, 在PyPI上唯一
    version='0.1.0',  # 初始版本号
    description='A file storage management package supporting various providers like S3, OSS, and Qiniu.',
    long_description=open('README.md').read(),  # 从 README.md 中读取包的详细描述
    long_description_content_type='text/markdown',  # README文件的类型
    author='duolabmeng6',
    author_email='1715109585@qq.com',
    url='https://github.com/duolabmeng6/efcFile',  # 项目主页
    packages=find_packages(),  # 自动查找包内所有的模块
    install_requires=[  # 项目的依赖包列表
        'boto3',
        'oss2',
        'qiniu',
        'python-dotenv'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords="efcFile",
    include_package_data=True,  # 包含包中的所有文件
    exclude_package_data={
        '': ['.env'],  # 排除 .env 文件
    },
)
