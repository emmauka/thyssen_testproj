import click
import psutil
import os
from tabulate import tabulate
import time


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
        cpu_usage = psutil.cpu_percent(interval=1)
        try:
            cpu_load = psutil.getloadavg()
        except AttributeError:
            cpu_load = "N/A on windows"

        table = [["Metric", "Value"],
                 ["CPU Usage (%)", cpu_usage],
                 ["CPU Load (1, 5, 15 min)", cpu_load]]

        click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))

        if not watch:
            break
        time.sleep(1)
        click.clear()

# Memory Command with Watch Option
@click.command()
@click.option('-w', '--watch', is_flag=True, help="Continuously watch memory usage.")
def memory(watch):
    """Show memory usage, total memory, and available memory."""
    while True:
        mem = psutil.virtual_memory()
        table = [["Metric", "Value"],
                 ["Total Memory (GB)", f"{mem.total / (1024 ** 3):.2f}"],
                 ["Available Memory (GB)", f"{mem.available / (1024 ** 3):.2f}"],
                 ["Memory Usage (%)", f"{mem.percent}"]]

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
        net_io = psutil.net_io_counters()
        table = [["Metric", "Value"],
                 ["Bytes Sent (MB)", f"{net_io.bytes_sent / (1024 ** 2):.2f}"],
                 ["Bytes Received (MB)", f"{net_io.bytes_recv / (1024 ** 2):.2f}"]]

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
        cpu_usage = psutil.cpu_percent(interval=1)  # Measures the span
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        table = [["Metric", "Value"],
                 ["CPU Usage (%)", cpu_usage],
                 ["Memory Usage (%)", mem.percent],
                 ["Disk Usage (%)", disk.percent]]
        click.clear()
        click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))

        if not watch:  # If not watch mean if -w flag is not provided, then it will show just once and break and not run continously as in real time
            break
        time.sleep(1)

# Disk Command
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