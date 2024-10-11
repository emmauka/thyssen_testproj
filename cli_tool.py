import click
import psutil  # Import psutil for system information (e.g., CPU, memory, disk)
import json  # Import json for handling JSON data
import shutil  # Import shutil for file operations like copy
import os  # Import os for file and directory handling
from tabulate import tabulate

# Constant for the default JSON path
DEFAULT_JSON_PATH = "C:/Users/emmau/thyssen_testproj/default.json"  # Standard path used when --file is not specified


# Define the helper function to print JSON data from a file
def json_print_file(file_path):
    """
    This function reads the JSON file from the specified file path and displays its contents.

    Args:
        file_path (str): The path to the JSON file to be printed.
    """
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            formatted_json = json.dumps(json_data, indent=4)
            print(formatted_json)
    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at path '{file_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Define the 'json-copy' subcommand to copy JSON files
@click.command()
@click.option('--file', type=click.Path(exists=True), help="Path to the JSON file to copy to the current directory.")
def json_copy(file):
    """
    Copies the JSON file specified by --file to the current working directory.
    """
    if not file:
        click.echo("Error: Please provide a JSON file path using the --file option.")
        return

    try:
        file_name = os.path.basename(file)
        destination_path = os.path.join(os.getcwd(), file_name)
        shutil.copy(file, destination_path)
        click.echo(f"Successfully copied '{file}' to '{destination_path}'.")
    except FileNotFoundError:
        click.echo(f"Error: The file at path '{file}' was not found.")
    except PermissionError:
        click.echo(f"Error: Permission denied when trying to copy '{file}'.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")


@click.command()
@click.option('--file', type=click.Path(exists=True), help="Path to the JSON file to modify.")
@click.option('--Key', type=str, required=True, help="Key to update in the JSON file.")
@click.option('--Value', type=str, required=True, help="New value for the specified key.")
def json_modify(file, key, value):
    """Modify the value of a specified key in the JSON file."""
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        data[key] = value
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
        click.echo(f"Successfully updated '{key}' in '{file}' with new value: '{value}'.")
    except Exception as e:
        click.echo(f"Error modifying the file: {e}")


@click.command()
@click.option('--file', type=click.Path(exists=True), help="Path to the JSON file to delete.")
def json_delete(file):
    """Delete the specified JSON file."""
    try:
        os.remove(file)
        click.echo(f"Successfully deleted '{file}'.")
    except Exception as e:
        click.echo(f"Error deleting the file: {e}")



# Define the main command group with the `invoke_without_command=True` parameter
@click.group(invoke_without_command=True)
@click.option('--hello', is_flag=True, help="Say hello.")  # Define a global option for the CLI tool
@click.pass_context
def cli(ctx, hello):
    """
    Main entry point for the 'sil' command group with subcommands and options.
    This command group provides subcommands like `cpu`, `memory`, `disk`, and `json-output`.
    The `--hello` option displays a greeting message when used.
    """
    if hello:
        click.echo("Hello, World!")
        return  # Exit after displaying the greeting message

    if ctx.invoked_subcommand is None:
        click.echo("Use --hello for a greeting or use one of the available subcommands.")
        click.echo(ctx.get_help())  # Display help message when no subcommand is invoked


# Define the 'cpu' subcommand to display CPU usage and load
@click.command()
def cpu():
    """Display CPU usage and system load."""
    cpu_usage = psutil.cpu_percent(interval=1)
    try:
        cpu_load = psutil.getloadavg()
    except AttributeError:
        cpu_load = "N/A on windows"

    table = [["Metric", "Value"],
             ["CPU Usage (%)", cpu_usage],
             ["CPU Load (1, 5, 15 min)", cpu_load]]

    click.echo(tabulate(table, headers="firstrow", tablefmt="grid"))


# Define the 'memory' subcommand to display memory usage information
@click.command()
def memory():
    """Show memory usage, total memory, and available memory."""
    mem = psutil.virtual_memory()
    click.echo(f"Total Memory: {mem.total / (1024 ** 3):.2f} GB")
    click.echo(f"Available Memory: {mem.available / (1024 ** 3):.2f} GB")
    click.echo(f"Memory Usage: {mem.percent}%")


# Define the 'disk' subcommand to display disk usage and space details
@click.command()
def disk():
    """Show disk usage, total space, and free space."""
    disk_usage = psutil.disk_usage('/')
    click.echo(f"Total Disk Space: {disk_usage.total / (1024 ** 3):.2f} GB")
    click.echo(f"Used Disk Space: {disk_usage.used / (1024 ** 3):.2f} GB")
    click.echo(f"Free Disk Space: {disk_usage.free / (1024 ** 3):.2f} GB")


# Define the 'json-output' subcommand to display or save JSON data
@click.command()
@click.option('--file', type=click.Path(exists=True), help="Path to a JSON file to display its contents.")
@click.option('--save', type=click.Path(), help="Path to save the JSON output instead of displaying it.")
@click.option('--pretty', is_flag=True, help="Pretty-print the JSON output with indentation.")
def json_output(file, save, pretty):
    """
    Display sample JSON data or read from a specified JSON file.
    Use the --file option to provide a path to a JSON file. If no file is provided, it displays default sample JSON data.
    Use the --save option to save the output to a file instead of displaying it.
    Use the --pretty option to format the JSON with indentation.
    """
    # Load JSON data either from a file or use the default sample data
    if file:
        with open(file, 'r') as f:
            data = json.load(f)
    else:
        # Use the default JSON data if no file is provided
        if os.path.exists(DEFAULT_JSON_PATH):
            click.echo(f"No file provided. Displaying JSON data from the default path: {DEFAULT_JSON_PATH}")
            with open(DEFAULT_JSON_PATH, 'r') as f:
                data = json.load(f)
        else:
            click.echo(f"No file provided and the default JSON file '{DEFAULT_JSON_PATH}' does not exist.")
            click.echo("Displaying sample JSON data instead.")
            data = {
                "TestKey": "Value",
                "Nested": {
                    "NestKey": "Val",
                    "Iteration": 1
                }
            }

    # Format the JSON data based on the --pretty option
    json_str = json.dumps(data, indent=4) if pretty else json.dumps(data)

    # Save to file if --save is specified, otherwise display in console
    if save:
        with open(save, 'w') as save_file:
            save_file.write(json_str)
        click.echo(f"JSON data has been saved to '{save}'.")
    else:
        click.echo("Displaying JSON data:")
        click.echo(json_str)


# Attach the commands to the cli group
cli.add_command(cpu)
cli.add_command(memory)
cli.add_command(disk)
cli.add_command(json_output)
cli.add_command(json_copy)

# Main entry point to run the command group
if __name__ == '__main__':
    cli()