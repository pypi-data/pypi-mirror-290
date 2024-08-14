from setuptools import setup, find_packages

setup(
    name="multi_db_query_builder",
    version="0.1.4",
    description="Simplify SQL queries across databases",
    author="Mukesh Prasad",
    author_email="mukesh@stepfunction.ai",
    url="https://bitbucket.org/ChandaniStepFunction/db_query_builder",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "SQLAlchemy==1.4.16",
        "snowflake-connector-python==3.2.1",
        "snowflake-snowpark-python==1.10.0",
        "snowflake-sqlalchemy==1.5.0",
        "sqlalchemy-bigquery==1.10.0",
        "sqlalchemy-redshift==0.8.14",
        "redshift-connector==2.1.0",
        "psycopg2-binary==2.9.2",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
