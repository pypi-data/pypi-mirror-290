import os
import sys
import json
import traceback
import importlib
import inspect

import click
import yaml

from .access import *
from .specification import *
from .lib import *


def load_modules_from_config(config_path):
    """
    Load Python modules from paths specified in a YAML configuration file.
    """
    try:
        if config_path is None:
            # Nothing to do
            return

        if not os.path.exists(config_path):
            return

        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

            module_paths = config.get('module_paths', [])
            for path in module_paths:
                if path not in sys.path:
                    sys.path.append(path)
            return config
    except Exception as e:
        traceback.print_exc()
        print(f"Failed to load modules from config: {str(e)}")


def load_subclass(module_name,
                  defaultclass=StandardDataSourceLoader,
                  baseclass=DataSourceLoader):
    """
    Load the subclass of Specification from the specified module.
    """

    if module_name is None:
        return defaultclass

    module = importlib.import_module(module_name)
    subclasses = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, baseclass) and obj is not baseclass:
            subclasses.append(obj)
    if not subclasses:
        raise ValueError("No subclass of Specification found in the module.")
    return subclasses[0]  # Assuming there's only one subclass and returning it


@click.group()
@click.option(
    '--config',
    default='evalgen.yaml',
    help='Path to the configuration YAML file containing module paths'
)
def main(config):
    """
    EvalGen CLI: A command-line interface for generating and applying
    data transformation specifications.
    """
    config = load_modules_from_config(config)


@main.command()
@click.option('--loader-class', help='Full path to the loader class (e.g., package.module.ClassName)')
@click.option('--input-type', help='Specify input type (csv, json, jsonl, log, database, url) if automatic inference is incorrect')
@click.option('--input-path', required=True, help='Path to the input data source')
@click.option('--source-config', help='Path to a YAML file containing source-specific configuration')
@click.option('--output-file', help='Path to the output Python file for the specification')
def generate_spec(loader_class, input_path,
                  input_type, source_config,
                  output_file):
    """
    Generate a specification by interacting with the user to select columns and transformations.
    """
    try:

        # Source handler..
        sourceclass = load_subclass(loader_class)
        instance = sourceclass()

        # Load source configuration if provided
        source_options = {}
        if source_config:
            with open(source_config, 'r') as f:
                source_options = yaml.safe_load(f)

        # Create a simple spec object to pass source options
        class SimpleSpec:

            def get_csv_options(self):
                return source_options.get('csv', {})
            def get_json_options(self):
                return source_options.get('json', {})
            def get_jsonl_options(self):
                return source_options.get('jsonl', {})
            def get_log_options(self):
                return source_options.get('log', {})
            def get_db_options(self):
                return source_options.get('database', {})
            def get_url_options(self):
                return source_options.get('url', {})

        # Double check if all is well..
        instance.validate(input_path)

        df, params = instance.load(input_path, input_type, spec=SimpleSpec())
        # print("Params", json.dumps(params, indent=4))

        code = generate_specification(instance, df, params)

        # Write the specification to a Python file
        if output_file is not None:
            with open(output_file, 'w') as f:
                f.write(code)
            print(f"Specification saved to {output_file}")
        else:
            print("Generated Code Snippet:")
            print(code)

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {str(e)}")

@main.command()
@click.option('--loader-class', help='Full path to the loader class (e.g., package.module.ClassName)')
@click.option('--spec-class', required=False, help='Full path to the loader class (e.g., package.module.ClassName)')
@click.option('--input-path', required=True, help='Path to the input data source')
@click.option('--input-type', help='Specify input type (csv, json, jsonl, log, database, url) if automatic inference is incorrect')
@click.option('--source-config', help='Path to a YAML file containing source-specific configuration')
@click.option('--output-file', help='Path to the output JSON file')
def apply_spec(loader_class, spec_class, input_path, input_type, source_config, output_file):
    """
    Apply a specification to transform data.
    """
    try:
        specclass = load_subclass(spec_class,
                                  defaultclass=Specification,
                                  baseclass=Specification)
        specinstance = specclass()
        sourceclass = load_subclass(loader_class,
                                    defaultclass=StandardDataSourceLoader,
                                    baseclass=DataSourceLoader)
        instance = sourceclass()

        # Load source configuration if provided
        source_options = {}
        if source_config:
            with open(source_config, 'r') as f:
                source_options = yaml.safe_load(f)

        # Add source options to the spec instance
        for source_type, options in source_options.items():
            set_method = f'set_{source_type}_options'
            if hasattr(specinstance, set_method):
                getattr(specinstance, set_method)(options)

        df, params = instance.load(input_path, spec=specinstance)

        transformed_df = apply_specification(df, specinstance)

        if output_file is not None:
            transformed_df.to_json(output_file, orient='records', lines=True)
            print(f"Data successfully transformed and saved to {output_file}")
        else:
            print(transformed_df.to_json(orient='records', lines=True))

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {str(e)}")

@main.command()
@click.option(
    "--output-file",
    type=click.Path(),
    default=None,
    help='Path to the output file for the sample source configuration.'
)
def sample_source_config(output_file):
    """
    Generate a sample source configuration YAML file.
    """
    sample_config = {
        'csv': {
            'chunksize': 10000,
            'usecols': ['column1', 'column2'],
            'nrows': 100000,
            'skiprows': 1,
            'encoding': 'utf-8',
        },
        'json': {
            'orient': 'records',
            'lines': False,
            'encoding': 'utf-8',
            'nrows': 100000,
        },
        'jsonl': {
            'chunksize': 10000,
            'nrows': 100000,
            'encoding': 'utf-8',
        },
        'log': {
            'delimiter': r'\s+',
            'names': ['timestamp', 'level', 'message'],
            'parse_dates': ['timestamp'],
            'nrows': 100000,
            'skiprows': 1,
        },
        'database': {
            'table': 'your_table_name',
            'columns': ['column1', 'column2'],
            'where': 'column1 > 100',
            'limit': 100000,
        },
        'url': {
            'nrows': 100000,
            'usecols': ['column1', 'column2'],
            'skiprows': 1,
            'encoding': 'utf-8',
        }
    }
    yaml_content = yaml.dump(sample_config, default_flow_style=False)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(yaml_content)
        print(f"Sample source configuration written to {output_file}")
    else:
        print("Sample source configuration:\n", file=sys.stderr)
        print(yaml_content)


if __name__ == '__main__':
    main()
