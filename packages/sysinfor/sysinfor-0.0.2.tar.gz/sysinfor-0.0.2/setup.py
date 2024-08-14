from setuptools import setup, find_packages
LONG_DESCRIPTION = """
A package of ***sysinfor*** is use to display system information.Generally it available bellow information on initial release.
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
"""
setup(
    name="sysinfor",
    version="0.0.2",
    description="A package of ***sysinfor*** is use to display system information.",
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