from setuptools import setup, find_packages

setup(
    name="pyeqx",
    version="0.4.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "adlfs==2023.8.0",
        "azure-identity>=1.13.0",
        "azure-storage-blob>=12.16.0",
        "azure-storage-file-datalake>=12.11.0",
        "azure-storage-queue>=12.6.0",
        "delta-spark>=2.3.0,<2.4.0",
        "minio>=7.2.3",
        "numpy>=1.26.0",
        "pandas>=2.1.1",
        "psycopg2-binary>=2.9.9",
        "pymssql>=2.2.11",
        "pyspark>=3.3.4,<3.4.0",
        "requests>=2.30.0",
        "tenacity>=8.2.1",
    ],
    python_requires=">=3.9",
)
