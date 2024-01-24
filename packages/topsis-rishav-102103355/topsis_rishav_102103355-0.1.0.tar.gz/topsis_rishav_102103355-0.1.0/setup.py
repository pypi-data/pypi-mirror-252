# setup.py
import pathlib
from setuptools import setup, find_packages

setup(
    name='topsis_rishav_102103355',
    version='0.1.0',
    packages=find_packages(),
    long_description= pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'topsis = topsis.topsis:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
