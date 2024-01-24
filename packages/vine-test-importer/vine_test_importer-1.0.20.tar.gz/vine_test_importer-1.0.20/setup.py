from setuptools import setup, find_packages


with open('importers/README.md', encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'pip',
    'numpy',
    'requests',
    'pandas',
    'curlify',
    'PyYAML',
    'psycopg2-binary',
    'pymysql',
    'pyhive',
    'thrift',
    'sasl'
]

setup(
    name='vine_test_importer',
    version='1.0.20',
    description='GrowingIO Importer是GrowingIO CDP平台元数据创建和数据导入工具',
    author='vine_wang',
    author_email='vine_wc@163.com',
    packages=find_packages(include=["importers*"]),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        # 'Development Status :: 3 - Alpha',  # 发布开发版分类器
        'Development Status :: 5 - Production/Stable',  # 发布稳定版分类器
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'clear_user=importers.clear_user:main',
            'data_importer=importers.data_importer:main',
            'format_importer=importers.format_importer:main',
            'meta_importer=importers.meta_importer:main',
        ],
    },
)
