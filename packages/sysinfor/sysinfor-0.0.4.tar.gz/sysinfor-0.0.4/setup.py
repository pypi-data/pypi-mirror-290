from setuptools import setup, find_packages
LONG_DESCRIPTION = """
A package of **sysinfor** is use to display system information.Generally it available bellow information on initial release.
    - OS Kernel
    - Node Name(user)
    - OS Release
    - OS Version
    - Machine Architecture
    - Processor
    - CPU Count
    - Username
    - Physical Menory
    - Python version

## Installation

You can install the package using `pip`:

```bash
$ pip install .
```

## Testing
```bash
$ python -m unittest discover tests
```

## Commands
```bash
$ sysinfor --all
```
```
System Information:
Kernel: Linux
Node Name: core
Release: 5.10.0-30-amd64
Version: #1 SMP Debian 5.10.218-1 (2024-06-01)
Processor: 
Arch: x86_64
Boot Time: 2024-07-31 09:29:00
Physical CPU Count: 10
Memory: 8 GB
Python Version: 3.9.2 (default, Feb 28 2021, 17:03:44) 
[GCC 10.2.1 20210110]
```
"""
setup(
    name="sysinfor",
    version="0.0.4",
    description="The package of **SysInfor** is use to collect & manipulate system information for human friendly manner.",
    long_description=LONG_DESCRIPTION,
    author="Tharanga Jayasinghe",
    author_email="nteeje@gmail.com",
    packages=find_packages(),
    install_requires=[
        "psutil","click","datetime"
    ],
    entry_points={
        "console_scripts": [
            "sysinfor=sysinfor.info:main",
        ],
    },
)