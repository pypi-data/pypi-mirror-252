"""
This module sets up the hue_entertainment_pykit package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hue_entertainment_pykit",
    version="0.7",
    author="Dominik Hrdas",
    author_email="hrdasdominik@gmail.com",
    description="A comprehensive Python toolkit for Philips Hue Entertainment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hrdasdominik/hue-entertainment-pykit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "colorama==0.4.6",
        "idna==3.6",
        "ifaddr==0.2.0",
        "mypy-extensions==1.0.0",
        "packaging==23.2",
        "pathspec==0.12.1",
        "platformdirs==4.1.0",
        "python-mbedtls==2.8.0",
        "requests==2.31.0",
        "typing_extensions==4.9.0",
        "urllib3==2.1.0",
        "zeroconf==0.131.0",
    ],
)
