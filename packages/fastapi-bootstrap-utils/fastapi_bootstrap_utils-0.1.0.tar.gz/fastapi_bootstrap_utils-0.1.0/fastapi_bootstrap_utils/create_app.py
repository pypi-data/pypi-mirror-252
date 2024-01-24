#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a simple REST API from a tab-delimited data file."""
import click
import logging
import json
import os
import pathlib
import sys
import yaml

from rich.console import Console
from datetime import datetime
from typing import Any, Dict, Optional

from .console_helper import print_red, print_yellow, print_green
from .file_utils import check_infile_status


DEFAULT_PROJECT = "fastapi-bootstrap-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR = os.path.join(
    "/tmp/",
    os.getenv("USER"),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    DEFAULT_TIMESTAMP,
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.getcwd(),
    'conf',
    'config.yaml'
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def get_action(method: str, action_lookup: Dict[str, Any], config_file: str) -> str:
    """Derive the action from the method.

    Args:
        method (str): The method i.e.: GET, POST, PUT, DELETE.
        action_lookup (Dict[str, Any]): The lookup containing the actions.
        config_file (str): The configuration file.

    Raises:
        Exception: If the method is not found in the action lookup.

    Returns:
        str: The action.
    """
    if method in action_lookup:
        action = action_lookup[method]
    else:
        raise Exception(f"Could not find method '{method}' in the action lookup '{action_lookup}' - review the configuration file '{config_file}'")
    return action


def get_desc(action: str, record_type: str, column_header: str, method: str, config_file: str) -> str:
    """Derive the description from the action.

    Args:
        action (str): The action.
        record_type (str): The record type.
        column_header (str): The column header.
        method (str): The method i.e.: GET, POST, PUT, DELETE.
        config_file (str): The configuration file.

    Raises:
        Exception: If the action is not supported.

    Returns:
        str: The description.
    """

    desc = None
    method = method.upper()

    if action.lower() == "retrieve":
        desc = f"Retrieve '{record_type}' records via the '{method}' method for '{column_header}'"
    elif action.lower() == "create":
        desc = f"Create a '{record_type}' record via the '{method}' method for '{column_header}'"
    elif action.lower() == "update":
        desc = f"Update '{record_type}' records via the '{method}' method for '{column_header}'"
    elif action.lower() == "remove":
        desc = f"Remove '{record_type}' records via the '{method}' method for '{column_header}'"
    else:
        raise Exception(f"Action '{action}' is not supported - review the configuration file '{config_file}'")

    return desc


def create_cache_files(
    infile: str,
    outdir: str,
    config_file: str,
    config: Dict[str, Any],
    verbose: bool = DEFAULT_VERBOSE) -> Dict[str, str]:
    """Create the cache files.

    Args:
        infile (str): The tab-delimited input file.
        outdir (str): The output directory.
        config_file (str): The configuration file.
        config (Dict[str, Any]): The configuration object.
        verbose (bool, optional): Whether to print verbose output. Defaults to DEFAULT_VERBOSE.

    Returns:
        str: The JSON file containing the cached records.
    """
    if verbose:
        console.print(f"Will create cache files for '{infile}'")
    logging.info(f"Will create cache files for '{infile}'")

    # Read the input tab-delimited file into a dictionary where the key is the column header and the value is the column index.
    column_header_lookup = {}

    line_ctr = 0
    column_header_list = None
    with open(infile, 'r') as f:
        # column_header_list = f.readline().strip().split('\t')
        for line in f:
            line_ctr += 1
            if line_ctr == 1:
                # Process the header line
                column_header_list = line.strip().split('\t')
                continue

            line = line.strip()
            record = line.split('\t')

            record_lookup = {}

            for i in range(len(record)):
                if column_header_list[i] in config["ignore_columns"]:
                    continue

                record_lookup[column_header_list[i]] = record[i]


            logging.info(f"record lookup: '{record_lookup}'")

            for column_header in column_header_list:
                if column_header in config["ignore_columns"]:
                    continue

                val = record_lookup[column_header]

                logging.info(f"Building cache record for column_header: {column_header} val '{val}'")

                if column_header not in column_header_lookup:
                    column_header_lookup[column_header] = {}
                if val not in column_header_lookup[column_header]:
                    column_header_lookup[column_header][val] = []

                column_header_lookup[column_header][val].append(record_lookup)

    outfile = os.path.join(outdir, "cache_file_lookup.json")

    lookup = {
        "method-created": os.path.abspath(__file__),
        "date-created": str(datetime.today().strftime('%Y-%m-%d-%H%M%S')),
        "created-by": os.environ.get('USER'),
        "infile": infile,
        "config_file": config_file,
        "records": column_header_lookup
    }

    # Write lookup to JSON file
    with open(outfile, 'w') as of:
        of.write(json.dumps(lookup, indent=4))

    logging.info(f"Wrote cached records to JSON file '{outfile}'")
    console.print(f"Wrote cached records to JSON file '{outfile}'")

    return outfile

def create_rest_api(
    infile: str,
    outdir: str,
    config_file: str,
    config: Dict[str, Any],
    logfile: str,
    record_type: str,
    verbose: bool = DEFAULT_VERBOSE) -> None:
    """Create the REST API service application.

    Args:
        infile (str): The tab-delimited input file.
        outdir (str): The output directory.
        config_file (str): The configuration file.
        config (Dict[str, Any]): The configuration object.
        logfile (str): The log file.
        record_type (str): The record type.
        verbose (bool, optional): Whether to print verbose output. Defaults to DEFAULT_VERBOSE.
    """
    # Get the column header list from the file.
    # This assumes that the first line of the file contains the column headers.
    column_header_list = pathlib.Path(infile).read_text().splitlines()[0].split('\t')

    cached_records_file = create_cache_files(
        infile,
        outdir,
        config_file,
        config,
        verbose
    )

    create_helper_module(
        cached_records_file,
        infile,
        outdir,
        config_file,
        config,
        logfile,
        verbose
    )


    app_lookup = {}

    if "methods" not in config:
        raise Exception(f"The 'methods' key is missing from the configuration file '{config_file}'")

    methods = config["methods"]

    # TODO: Add support for other datatypes
    datatype = "str"

    action_lookup = config["action_lookup"]

    route_lookup = {}

    for column_header in column_header_list:

        if column_header in config["ignore_columns"]:
            logging.info(f"Will ignore column header '{column_header}' based on configuration")
            continue

        if "datatypes" in config:
            if column_header in config["datatypes"]:
                datatype = config["datatypes"][column_header]
            else:
                logging.warning(f"Could not find column header '{column_header}' in the datatypes lookup - will use the default datatype '{datatype}'")
                print_yellow(f"Could not find column header '{column_header}' in the datatypes lookup - will use the default datatype '{datatype}'")


        cleaned_column_header = column_header.replace(" ", "_").replace("#", "").replace("-", "_").lower()



        for method in methods:

            action = get_action(method, action_lookup, config_file)

            desc = get_desc(action, record_type, column_header, method, config_file)

            create_endpoints(
                app_lookup,
                column_header,
                method,
                action,
                datatype,
                # config,
                desc,
                cleaned_column_header,
                verbose
            )



    # route_module_file = os.path.join(
    #     outdir,
    #     record_type.lower(),
    #     f"{cleaned_column_header}_router.py"
    # )

    # if column_header not in route_lookup:

    #     module_basename = f"{cleaned_column_header}_router"
    #     import_statement = f"from {record_type.lower()}.{module_basename} import router as {module_basename}"
    #     route_statement = f"app.include_router({module_basename}, prefix=\"/{record_type.lower()}/{cleaned_column_header}\", tags=[\"{record_type.lower()} by {cleaned_column_header}\"])"

    #     route_lookup[column_header] = {
    #         "import": import_statement,
    #         "route": route_statement
    #     }

    route_module_file = os.path.join(
        outdir,
        record_type.lower(),
        f"{record_type.lower()}_router.py"
    )

    module_basename = f"{record_type.lower()}_router"
    import_statement = f"from {record_type.lower()}.{module_basename} import router as {module_basename}"
    route_statement = f"app.include_router({module_basename}, prefix=\"/{record_type.lower()}\", tags=[\"{record_type.lower()}\"])"

    route_lookup[record_type.lower()] = {
        "import": import_statement,
        "route": route_statement
    }


    create_route_module(
        route_module_file,
        app_lookup,
        outdir,
        config_file,
        config,
        infile,
        logfile,
        verbose,
    )


    create_main_file(
        route_lookup,
        outdir,
        config_file,
        config,
        infile,
        logfile,
        verbose
    )


def create_route_module(
    outfile: str,
    app_lookup: Dict[str, Any],
    outdir: str,
    config_file: str,
    config: Dict[str, Any],
    infile: str,
    logfile: str,
    verbose: bool = DEFAULT_VERBOSE) -> None:
    """Create the route module.

    Args:
        outfile (str): The route module file.
        app_lookup (Dict[str, Any]): The lookup containing the routes and methods.
        outdir (str): The output directory.
        config_file (str): The configuration file.
        config (Dict[str, Any]): The configuration object.
        infile (str): The tab-delimited input file.
        logfile (str): The log file.
        verbose (bool, optional): _description_. Defaults to DEFAULT_VERBOSE.
    """
    router_dir = os.path.dirname(outfile)
    if not os.path.exists(router_dir):
        pathlib.Path(router_dir).mkdir(parents=True, exist_ok=True)
        if verbose:
            print_yellow(f"Created output directory '{router_dir}'")
        logging.info(f"Created output directory '{router_dir}'")

    template_file = get_template_file("router", config_file, config)

    line_ctr = 0

    with open(template_file, 'r') as f, open(outfile, 'w') as of:

        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## infile: {infile}\n")
        of.write(f"## config_file: {config_file}\n")
        of.write(f"## logfile: {logfile}\n\n")


        for line in f:
            line_ctr += 1
            line = line.strip()
            of.write(f"{line}\n")
            if line.startswith("# INSERT FUNCTIONS HERE"):
                for route in app_lookup:
                    for method in app_lookup[route]:
                        of.write(f"{app_lookup[route][method]}\n")

    if line_ctr > 0:
        logging.info(f"Read '{line_ctr}' lines from file '{template_file}'")

    console.print(f"Created main application file [bold green]'{outfile}'[/]")



def get_template_file(
    file_type: str,
    config_file: str,
    config: Dict[str, Any]) -> str:
    """Get the template file.

    Args:
        file_type (str): The type of file i.e.: main, helper_module.
        config_file (str): The configuration file.
        config (Dict[str, Any]): The configuration object.
    Returns:
        str: The template file.
    """
    if "template_files" not in config:
        raise Exception(f"The 'template_files' key is missing from the configuration file '{config_file}'")

    if file_type not in config["template_files"]:
        raise Exception(f"The '{file_type}' key is missing from the configuration file '{config_file}'")

    template_file = config["template_files"][file_type]

    check_infile_status(template_file, "py.tt")

    return template_file


def create_main_file(
    route_lookup: Dict[str, Dict[str, Any]],
    outdir: str,
    config_file: str,
    config: Dict[str, Any],
    infile: str,
    logfile: str,
    verbose: bool = DEFAULT_VERBOSE) -> None:
    """Create the main app file.

    Args:
        route_lookup (Dict[str, Dict[str, str]]): The lookup containing the import statements and route statements.
        outdir (str): The output directory.
        config_file (str): The configuration file.
        config (Dict[str, Any]): The configuration object.
        infile (str): The tab-delimited input file.
        logfile (str): The log file.
        verbose (bool, optional): Whether to print verbose output. Defaults to DEFAULT_VERBOSE.

    Raises:
        Exception: If the template file is not specified in the configuration file.
    """
    outfile = os.path.join(outdir, "main.py")

    template_file = get_template_file("main", config_file, config)

    line_ctr = 0

    with open(template_file, 'r') as f, open(outfile, 'w') as of:

        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## infile: {infile}\n")
        of.write(f"## config_file: {config_file}\n")
        of.write(f"## logfile: {logfile}\n\n")


        for line in f:
            line_ctr += 1
            line = line.strip()
            of.write(f"{line}\n")
            if line.startswith("# INSERT ROUTES HERE"):
                for record_type in route_lookup:
                    of.write(f"{route_lookup[record_type]['import']}\n")
                of.write("\n\n")
                for record_type in route_lookup:
                    of.write(f"{route_lookup[record_type]['route']}\n")

    if line_ctr > 0:
        logging.info(f"Read '{line_ctr}' lines from file '{template_file}'")

    console.print(f"Created main application file [bold green]'{outfile}'[/]")


def create_endpoints(
    app_lookup: Dict[str, Any],
    column_header: str,
    method: str,
    action: str,
    datatype: str,
    desc: str,
    cleaned_column_header: str,
    # config: Dict[str, Any],
    # record_type: str,
    # config_file: str,
    verbose: bool = DEFAULT_VERBOSE) -> Dict[str, Any]:
    """Create the endpoints for the column header.

    Args:
        app_lookup (Dict[str, Any]): The lookup containing the routes and methods.
        column_header (str): The column header.
        method (str): The method i.e.: GET, POST, PUT, DELETE.
        datatype (str): The datatype of the column header.
        action (str): The action to be performed.
        config (Dict[str, Any]): The configuration object.
        record_type (str): The record type.
        config_file (str): The configuration file.
        verbose (bool, optional): Whether to print verbose output. Defaults to DEFAULT_VERBOSE.
    """
    if verbose:
        console.print(f"Creating [bold yellow]'{method.upper()}'[/] route for column header [bold yellow]'{column_header}'[/]")
    logging.info(f"Creating '{method.upper()}' route for column header '{column_header}'")

    route = cleaned_column_header

    if route not in app_lookup:
        app_lookup[route] = {}

    logging.info(f"Creating method '{method}' for route '{route}'")

    content = f"""@router.{method}(\"/{cleaned_column_header}/{{{route}_id}}\", description=\"{desc}\")
async def {method}_{route}({route}_id: {datatype}):
    if \"{column_header}\" in cached_records_lookup:
        if {route}_id in cached_records_lookup[\"{column_header}\"]:
            # results = json.dumps(cached_records_lookup[\"{column_header}\"][{route}_id])
            results = cached_records_lookup[\"{column_header}\"][{route}_id]
            return {{\"results\": results}}
    raise HTTPException(status_code=404, detail=f\"Could not find record for {column_header} {{{route}_id}}\")


"""


#     content = f"""@app.{method}(\"/{route}/{{{route}_id}}\", description=\"{desc}\")
# async def {method}_{route}({route}_id: {datatype}):
#     if \"{column_header}\" in cached_records_lookup:
#         if {route}_id in cached_records_lookup[\"{column_header}\"]:
#             # results = json.dumps(cached_records_lookup[\"{column_header}\"][{route}_id])
#             results = cached_records_lookup[\"{column_header}\"][{route}_id]
#             return {{\"results\": results}}
#     raise HTTPException(status_code=404, detail=f\"Could not find record for {column_header} {{{route}_id}}\")



    app_lookup[route][method] = content


def create_helper_module(
    cached_records_file: str,
    infile: str,
    outdir: str,
    config_file: str,
    config: Dict[str, Any],
    logfile: str,
    verbose: bool = DEFAULT_VERBOSE) -> None:
    """Create the helper module.

    Args:
        cached_records_file (str): The JSON file containing the cached records.
        infile (str): The tab-delimited input file.
        outdir (str): The output directory.
        config_file (str): The configuration file.
        config (Dict[str, Any]): The configuration object.
        logfile (str): The log file.
        verbose (bool, optional): Whether to print verbose output. Defaults to DEFAULT_VERBOSE.
    """
    outfile = os.path.join(outdir, "helper.py")

    template_file = get_template_file("helper", config_file, config)

    line_ctr = 0

    with open(template_file, 'r') as f, open(outfile, 'w') as of:

        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## infile: {infile}\n")
        of.write(f"## config_file: {config_file}\n")
        of.write(f"## logfile: {logfile}\n\n")

        for line in f:
            line_ctr += 1
            # line = line.strip()
            of.write(f"{line}")
            if line.startswith("# INSERT CACHE FILE"):
                of.write(f"CACHE_FILE = \"{cached_records_file}\"\n")

    if line_ctr > 0:
        logging.info(f"Read '{line_ctr}' lines from file '{template_file}'")

    console.print(f"Created helper module file [bold green]'{outfile}'[/]")


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'.")
@click.option('--infile', help="Required: The input tab-delimited data file.")
@click.option('--logfile', help="Optional: The log file.")
@click.option('--outdir', help=f"Optional: The output directory where the output files should be written - default is '{DEFAULT_OUTDIR}'.")
@click.option('--record_type', help="Optional: The type of record each row represents in the tab-delimited file.")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: Optional[str], infile: str, logfile: Optional[str], outdir: Optional[str], record_type: Optional[str], verbose: Optional[bool]):
    """Create a simple REST API from a tab-delimited data file."""
    error_ctr = 0

    if infile is None:
        print_red("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile, "tsv")

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    check_infile_status(config_file, "yaml")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    if verbose:
        console.print(f"Will load contents of config file '{config_file}'")
    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())

    if "record_type" not in config:
        raise Exception(f"The 'record_type' key is missing from the configuration file '{config_file}'")

    record_type = config["record_type"]

    create_rest_api(
        infile,
        outdir,
        config_file,
        config,
        logfile,
        record_type,
        verbose
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
