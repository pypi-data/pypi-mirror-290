import os

from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="ca-alerts-client",
    version="0.1",
    packages=find_packages(),
    python_requires='>=3.8',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        "pandas~=2.0.3",
        "dataframe-image~=0.2.4",
        "tenacity~=9.0.0",
        "lxml~=5.3.0",
        "openpyxl~=3.1.5",
        "setuptools~=72.1.0",
        "pika~=1.3.2",
        "matplotlib~=3.7.5"
    ]
)
