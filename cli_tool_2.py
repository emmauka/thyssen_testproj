import click
import time
import psutil
from tabulate import tabulate
from monitors.cpu_monitor import get_cpu_usage  # Import CPU monitor function
from monitors.memory_monitor import get_memory_usage  # Import Memory monitor function
from monitors.network_monitor import get_network_io  # Import Network monitor function
from monitors.system_monitor import get_system_usage  # Import System monitor function
import sys
import os

# Add the project root to the system path so Python can find the monitors module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Core CLI Commands
@click.group(invoke_without_command=True)
@click.option('--hello', is_flag=True, help="Say hello.")
@click.pass_context
def cli(ctx, hello):
    if hello:
        click.echo("Hello, World!")
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

# CPU Command with Watch Option
@click.command()
@click.option('-w', '--watch', is_flag=True, help="Continuously watch CPU usage.")
def cpu(watch):
    """Display CPU usage and system load."""
    while True:
        cpu_usage = get_cpu_usage()  # Using the modularized function
        table = [["Metric", "Value"],
                 ["CPU Usage (%)", cpu_usage]]

        click.clear()
        click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))

        if not watch:
            break
        time.sleep(1)

# Memory Command with Watch Option
@click.command()
@click.option('-w', '--watch', is_flag=True, help="Continuously watch memory usage.")
def memory(watch):
    """Show memory usage, total memory, and available memory."""
    while True:
        memory_stats = get_memory_usage()  # Using the modularized function
        table = [["Metric", "Value"]] + [[k, v] for k, v in memory_stats.items()]

        click.clear()
        click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))

        if not watch:
            break
        time.sleep(1)

# Network Monitor Command
@click.command(name='network_monitor')
@click.option('-w', '--watch', is_flag=True, help="Continuously monitor network bandwidth usage.")
def network_monitor(watch):
    """Monitor network bandwidth usage in real time."""
    while True:
        net_io = get_network_io()  # Using the modularized function
        table = [["Metric", "Value"]] + [[k, v] for k, v in net_io.items()]

        click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))

        if not watch:
            break
        time.sleep(1)

# System Monitor Command
@click.command(name='system_monitor')
@click.option('-w', '--watch', is_flag=True, help="Continuously monitor system usage.")
def system_monitor(watch):
    """Monitor CPU, Memory, and Disk usage in real time."""
    while True:
        system_stats = get_system_usage()  # Using the modularized function
        table = [["Metric", "Value"]] + [[k, v] for k, v in system_stats.items()]

        click.clear()
        click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))

        if not watch:
            break
        time.sleep(1)

# Disk Command (no changes needed here)
@click.command()
def disk():
    """Show disk usage, total space, and free space."""
    disk_usage = psutil.disk_usage('/')
    click.echo(f"Total Disk Space: {disk_usage.total / (1024 ** 3):.2f} GB")
    click.echo(f"Used Disk Space: {disk_usage.used / (1024 ** 3):.2f} GB")
    click.echo(f"Free Disk Space: {disk_usage.free / (1024 ** 3):.2f} GB")

# Attach the core commands
cli.add_command(cpu)
cli.add_command(memory)
cli.add_command(disk)
cli.add_command(network_monitor)
cli.add_command(system_monitor)

# Main entry point to run the command group
if __name__ == '__main__':
    cli()