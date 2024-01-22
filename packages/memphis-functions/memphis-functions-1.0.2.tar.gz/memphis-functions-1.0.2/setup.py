from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="memphis-functions",
    packages=["memphis"],
    version="1.0.2",
    license="Apache-2.0",
    description="A powerful messaging platform for modern developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    readme="README.md",
    author="Memphis.dev",
    author_email="team@memphis.dev",
    url="https://github.com/memphisdev/memphis-functions.py",
    download_url="https://github.com/memphisdev/memphis-functions.py/archive/refs/tags/1.0.2.tar.gz",
    keywords=["message broker", "devtool", "streaming", "data"],
    install_requires=[""],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
