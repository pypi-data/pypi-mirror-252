from setuptools import setup, find_packages


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
    version='1.0.14',
    author='vine_wang',
    author_email='vine_wc@163.com',
    packages=find_packages(''),  # 从importers目录中查找所有包
    package_dir={'': '../importers'},
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'clear_user=importers.clear_user:main',
            'data_importer=importers.data_importer:main',
            'format_importer=importers.format_importer:main',
            'meta_importer=importers.meta_importer:main',
        ],
    },
)
