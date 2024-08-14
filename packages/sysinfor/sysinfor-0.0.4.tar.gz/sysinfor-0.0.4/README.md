# System Information(SysInfor) Package for Pypi

A package of ***sysinfor*** is use to display system information.Generally it available bellow information on initial release.

* OS Kernel
* Node Name(user)
* OS Release
* OS Version
* Machine Architecture
* Processor
* Boot Time
* CPU Count
* Username
* Physical Memory
* Python Version

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
## Display all system information
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
```bash
## Get Help
sysinfor --help
```
```
Usage: sysinfor [OPTIONS]

  Display system technical information.

Options:
  --all      Display system related technical information
  --version  Show the version and exit.
  --help     Show this message and exit.
```
```bash
## Get sysinfor version
sysinfor --version
```
```
sysinfor, version 0.0.4
```