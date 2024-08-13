"""
This module provides classes for loading data from various sources.
It supports loading from CSV, JSON, JSONL, log files, databases, and URLs.
"""

import os
import pandas as pd
import importlib.util
from sqlalchemy import create_engine, inspect, text
from urllib.parse import urlparse
import re
import json
__all__ = [
    'DataSourceLoader',
    'StandardDataSourceLoader'
]

class DataSourceLoader:
    """
    Base class for data source loaders.
    """
    def validate(self):
        """
        Placeholder method for input validation.
        To be implemented by subclasses.
        """
        pass

class StandardDataSourceLoader(DataSourceLoader):
    """
    A flexible data loader that supports various input types and sources.
    """

    def __init__(self, config={}):
        """
        Initialize the StandardDataSourceLoader.

        Args:
            config (dict): Configuration dictionary for the loader.
        """
        self.config = {}

    def validate(self, input_path):
        """
        Validate the input path.

        Args:
            input_path (str): The path or URL to the input data.

        Raises:
            Exception: If the input path is invalid.
        """
        if input_path is None:
            raise Exception("StandardDataSourceLoader requires a valid path/url")
        if isinstance(input_path, str) and len(input_path) == 0:
            raise Exception(f"Invalid input path: {input_path}")
        if ((not os.path.exists(input_path)) and (input_path not in os.environ) and
            not input_path.startswith(('http://', 'https://', 'sqlite:///', 'postgresql://'))):
            raise Exception(f"Invalid input path: {input_path}. Path should be valid, an environment variable, or a valid URL/database connection string")

    def load(self, input_path, input_type=None, spec=None):
        """
        Load data from the specified input path.

        Args:
            input_path (str): The path or URL to the input data.
            input_type (str, optional): The type of input data. If None, it will be inferred.
            spec (object, optional): An object containing loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.

        Raises:
            Exception: If DBURL is not set in the environment when required.
        """
        self.validate(input_path)

        if input_path in os.environ:
            input_path = os.environ[input_path]

        if input_path == "DBURL":
            print("DBURL must be set in the environment")
            raise Exception("DBURL not set")

        input_type = self._infer_input_type(input_path, input_type, spec)

        return self._load_by_input_type(input_path, input_type, spec)

    def _insert_meta(self, input_path, input_type, options, source="file"):
        """
        Insert metadata into the options dictionary.

        Args:
            input_path (str): The path or URL to the input data.
            input_type (str): The type of input data.
            options (dict): The options dictionary to update.
            source (str, optional): The source of the data. Defaults to "file".
        """
        options["__meta__"] = {
            "input_type": input_type,
            "source": source,
            "input_path": input_path
        }

    def _infer_input_type(self, input_path, input_type, spec=None):
        """
        Infer the input type if not provided.

        Args:
            input_path (str): The path or URL to the input data.
            input_type (str, optional): The type of input data.
            spec (object, optional): An object containing loading specifications.

        Returns:
            str: The inferred input type.
        """
        if input_type is not None:
            return input_type

        if ((spec is not None) and
            (hasattr(spec, 'get_params'))):
            params = spec.get_params()
            if (("__meta__" in params) and
                ("input_type" in params['__meta__'])):
                input_type = params['__meta__']['input_type']
                return input_type

        if input_path in os.environ:
            input_path = os.environ[input_path]

        if input_path.startswith(('sqlite:///', 'postgresql://')):
            return 'database'
        elif input_path.startswith(('http://', 'https://')):
            return 'url'
        else:
            _, ext = os.path.splitext(input_path)
            ext = ext.lower()
            if ext == '.csv':
                return 'csv'
            elif ext == '.json':
                return 'json'
            elif ext == '.jsonl':
                return 'jsonl'
            elif ext == '.log':
                return 'log'
            else:
                return 'unknown'

    def _load_by_input_type(self, input_path, input_type, spec):
        """
        Load data based on the input type.

        Args:
            input_path (str): The path or URL to the input data.
            input_type (str): The type of input data.
            spec (object): An object containing loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.

        Raises:
            ValueError: If the input type is unsupported or unknown.
        """
        if input_type == 'csv':
            return self._load_from_csv(input_path, spec)
        elif input_type == 'json':
            return self._load_from_json(input_path, spec)
        elif input_type == 'jsonl':
            return self._load_from_jsonl(input_path, spec)
        elif input_type == 'log':
            return self._load_from_logfile(input_path, spec)
        elif input_type == 'database':
            return self._load_from_database(input_path, spec)
        elif input_type == 'url':
            return self._load_from_url(input_path, spec)
        else:
            raise ValueError(f"Unsupported or unknown input type: {input_type}")

    def _load_from_csv(self, input_path, spec):
        """
        Load data from a CSV file.

        Args:
            input_path (str): The path to the CSV file.
            spec (object): An object containing CSV loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.
        """
        csv_options = spec.get_csv_options() if spec and hasattr(spec, 'get_csv_options') else {}

        # Default options
        options = {
            "__meta__": {
                "input_type": "csv",
                "source": "file"
            },
            'chunksize': None,
            'usecols': None,
            'nrows': None,
            'skiprows': None,
            'header': 'infer',
            'encoding': 'utf-8',
            'sep': ',',
            'quotechar': '"',
            'parse_dates': False,
        }
        options.update(csv_options)

        if options['chunksize']:
            chunks = pd.read_csv(input_path, **options)
            df = pd.concat(chunk for chunk in chunks)
        else:
            df = pd.read_csv(input_path, **options)

        return df, options

    def _load_from_json(self, input_path, spec):
        """
        Load data from a JSON file.

        Args:
            input_path (str): The path to the JSON file.
            spec (object): An object containing JSON loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.
        """
        json_options = spec.get_json_options() if spec and hasattr(spec, 'get_json_options') else {}

        # Default options
        options = {
            'orient': 'records',
            'lines': False,
            'encoding': 'utf-8',
            'nrows': None,
        }
        options.update(json_options)

        df = pd.read_json(input_path, **options)
        if options['nrows']:
            df = df.head(options['nrows'])

        input_type = "json"
        self._insert_meta(input_path, input_type, options)
        return df, options

    def _load_from_jsonl(self, input_path, spec):
        """
        Load data from a JSONL file.

        Args:
            input_path (str): The path to the JSONL file.
            spec (object): An object containing JSONL loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.
        """
        jsonl_options = spec.get_jsonl_options() if spec and hasattr(spec, 'get_jsonl_options') else {}

        # Default options
        options = {
            'lines': True,
            'orient': 'records',
            'encoding': 'utf-8',
            'chunksize': None,
            'nrows': None,
        }
        options.update(jsonl_options)

        if options['chunksize']:
            chunks = pd.read_json(input_path, **options)
            df = pd.concat(chunk for chunk in chunks)
        else:
            df = pd.read_json(input_path, **options)

        if options['nrows']:
            df = df.head(options['nrows'])

        input_type = "jsonl"
        self._insert_meta(input_path, input_type, options)

        return df, options

    def _load_from_logfile(self, input_path, spec):
        """
        Load data from a log file.

        Args:
            input_path (str): The path to the log file.
            spec (object): An object containing log file loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.
        """
        log_options = spec.get_log_options() if spec and hasattr(spec, 'get_log_options') else {}

        # Default options
        options = {
            'delimiter': r'\s+',
            'header': None,
            'names': None,
            'parse_dates': False,
            'date_parser': None,
            'custom_regex': None,
            'nrows': None,
            'skiprows': None,
        }
        options.update(log_options)

        if options['custom_regex']:
            with open(input_path, 'r') as file:
                lines = file.readlines()
            data = []
            for line in lines:
                match = re.match(options['custom_regex'], line)
                if match:
                    data.append(match.groupdict())
            df = pd.DataFrame(data)
        else:
            df = pd.read_csv(
                input_path,
                delimiter=options['delimiter'],
                header=options['header'],
                names=options['names'],
                parse_dates=options['parse_dates'],
                # date_parser=options['date_parser'],
                nrows=options['nrows'],
                skiprows=options['skiprows']
            )

        input_type = "log"
        self._insert_meta(input_path, input_type, options)

        return df, options

    def _load_from_database(self, input_path, spec):
        """
        Load data from a database.

        Args:
            input_path (str): The database connection string.
            spec (object): An object containing database loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.
        """
        db_options = spec.get_db_options() if spec and hasattr(spec, 'get_db_options') else {}

        # Default options
        options = {
            'table': None,
            'query': None,
            'limit': None,
            'columns': None,
            'where': None,
        }
        options.update(db_options)

        engine = create_engine(source)
        connection = engine.connect()

        if options['query']:
            query = options['query']
        else:
            if not options['table']:
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                options['table'] = self._prompt_user_for_table(tables)

            query = f"SELECT "
            if options['columns']:
                query += ", ".join(options['columns'])
            else:
                query += "*"

            query += f" FROM {options['table']}"

            if options['where']:
                query += f" WHERE {options['where']}"

            if options['limit']:
                query += f" LIMIT {options['limit']}"

        options['query'] = query

        df = pd.read_sql(text(query), connection)
        connection.close()

        input_type = "database"
        self._insert_meta(input_path, input_type, options, source="db")

        return df, options

    def _load_from_url(self, input_path, spec):
        """
        Load data from a URL.

        Args:
            input_path (str): The URL to load data from.
            spec (object): An object containing URL loading specifications.

        Returns:
            tuple: A tuple containing the loaded DataFrame and the options used for loading.
        """
        url_options = spec.get_url_options() if spec and hasattr(spec, 'get_url_options') else {}

        # Default options
        options = {
            'nrows': None,
            'usecols': None,
            'skiprows': None,
            'encoding': 'utf-8',
        }
        options.update(url_options)

        df = pd.read_csv(input_path, **options)

        self._insert_meta(input_path, "csv", options, source="url")

        return df, options

    def _prompt_user_for_table(self, tables):
        """
        Prompt the user to select a table from a list of available tables.

        Args:
            tables (list): A list of available table names.

        Returns:
            str: The name of the selected table.
        """
        print("Available tables:")
        for table in tables:
            print(f"- {table}")
        selected_table = input("Enter the name of the table you want to extract: ")
        while selected_table not in tables:
            print("Invalid table name. Please choose from the available tables.")
            selected_table = input("Enter the name of the table you want to extract: ")
        return selected_table

