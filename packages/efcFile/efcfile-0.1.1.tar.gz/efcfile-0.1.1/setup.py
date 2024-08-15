from setuptools import setup, find_packages

setup(
    name='efcFile',
    version='0.1.1',
    description='A file storage management package supporting various providers like S3, OSS, and Qiniu.',
    long_description=open('README.md').read(),  #
    long_description_content_type='text/markdown',
    author='duolabmeng6',
    author_email='1715109585@qq.com',
    url='https://github.com/duolabmeng6/efcFile',
    packages=find_packages(),
    install_requires=[
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
