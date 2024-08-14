
"""
Provides system related technical information.

System Information:
------------------
    System      : Linux
    Node Name   : core
    Release     : 5.10.0-30-amd64
    Version     : #1 SMP Debian 5.10.218-1 (2024-06-01)
    Machine     : x86_64
    Boot Time   : 2024-07-31 09:29:00
    CPU Count(p): 10
    Memory      : 8 GB
"""

import platform
import psutil
import click
import datetime

def get_system_info():
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Boot Time": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "Physical CPU Count": psutil.cpu_count(logical=False),
        "Memory": f"{round(psutil.virtual_memory().total / (1024 ** 3))} GB",
    }
    return info

def display_system_info():
    info = get_system_info()
    print("System Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    display_system_info()

@click.command()
@click.option('--all', is_flag=True, help='Display system related technical information')
@click.version_option('0.1.0')

def main(all):
    """Display system technical information."""
    if all:
        info = get_system_info()
        click.echo("System Information:")
        for key, value in info.items():
            click.echo(f"{key}: {value}")
    else:
        click.echo("Use '--all' to display system related technical information or '--help' for more options.")

if __name__ == "__main__":
    main()