# EvalGen

EvalGen is a Python package designed to generate evaluation datasets from various sources. It includes modules for database access, specification generation, and integration with OpenAI's language models.

Idea is to point the tool at some file/database and generate a
transformation specification that can be repeatedly applied to
generate updated datasets as new data comes in. 

---

**NOTE**

Not ready for production use. Work has just started on this. If this work is of interest to you, drop a note to [pingali@scribbledata.io](mailto:pingali@scribbledata.io)

---

## Features
- Connect to multiple sources including databases and files
- Allow custom transformation to be applied to these sources
- Generate transformation specification using LLM once and apply repeatedly
- Multiple LLMs supported
- Most of this repo's code is written by LLM :)


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/evalgen.git
   cd evalgen

## Execution
```bash
$ evalgen
Usage: evalgen [OPTIONS] COMMAND [ARGS]...

  EvalGen CLI: A command-line interface for generating and applying data
  transformation specifications.

Options:
  --help  Show this message and exit.

Commands:
  apply-spec     Apply a specification to transform data.
  generate-spec  Generate a specification by interacting with the user to..
```
## Example 1

First generate the code snippet for transformation specification and store it in `spec.py`

```
$ evalgen generate-spec --loader-param .../data.csv
Available columns:
-------  -------  ------------------------------------------------------------------------
dt       object   ['2024-06-01 06:33:18.', '2024-06-01 07:13:22.', '2024-06-02 03:01:08.']
xid      object   ['XL000093954855', 'XY000093954855', 'MY000093954855']
status   object   ['R2', 'D2']
source   object   ['alpha', 'beta', 'theta']
content  object   ['After removing used ', 'End connection', '[Alpha] St']
-------  -------  ------------------------------------------------------------------------
Enter comma-separated column names to include [dt,xid,status,source,content]: source, content
Describe the transformation you want to apply
select rows that have transaction mentioned in them. Select both the source and content columns

Generated Code Snippet:

from evalgen import Specification

class GeneratedSpecification(Specification):

    def transform(self, df):
        transformed_df = df[df['content'].str.contains('transaction')][['source', 'content']]
        return transformed_df

```

Now apply the specific

```
$ evalgen apply-spec  --spec-class spec --loader-param .../data.csv
{"source":"alpha","content":"Transaction to Chile : amount 1000 "}
{"source":"alpha","content":"checking the route availability"}
...
```

## Example 2

```
# Set the env variable
$ export DBURL="sqlite:////home/.../cars.sqlite"

# Pass the env variable or pass the full path
$ evalgen apply-spec --spec-class cars --loader-param DBURL
Available tables:
- cars1
- cars1_anonymized
- cars2
Enter the name of the table you want to extract: cars1
Available data:
-----------------------------------------------  -------  ------------------------------------------------------------------------
Height                                           float64  ['61.0', '96.0', '104.0']
Dimensions Length                                float64  ['19.0', '93.0', '28.0']
Dimensions Width                                 float64  ['189.0', '143.0', '85.0']
Engine Information Driveline                     object   ['Rear-wheel drive', 'All-wheel drive', 'Front-wheel drive']
Engine Information Engine Type                   object   ['Nissan 3.7L 6 Cylind', 'Volkswagen 2.5L 5 Cy', 'Hyundai 3.5L 6 Cylin']
...
-----------------------------------------------  -------  ------------------------------------------------------------------------
Describe the transformation you want to apply
Select all cars with horsepower > 150.
For these cars multiply the mpg by 1.5
select identification year, mpg columns
...

from evalgen import Specification
import pandas as pd

class GeneratedSpecification(Specification):

    def get_query_params(self):
        '''
        Query parameters used to select data
        '''
        return {"table": "cars1", "limit": 1000}

    def transform(self, df):
        # Select all cars with horsepower > 150
        df = df[df['Engine Information Engine Statistics Horsepower'] > 150]

        # Multiply mpg by 1.5
        df['Fuel Information City mpg'] = df['Fuel Information City mpg'] * 1.5
        df['Fuel Information Highway mpg'] = df['Fuel Information Highway mpg'] * 1.5

        # Select identification year and mpg columns
        df = df[['Identification Year', 'Fuel Information City mpg', 'Fuel Information Highway mpg']]

        # Rename columns
        df = df.rename(columns={'Identification Year': 'Year', 'Fuel Information City mpg': 'City mpg', 'Fuel Information Highway mpg': 'Highway mpg'})

        return df

```

Store the above transformation specification somewhere where the
script can find it. You add the directory to the module paths in evalgen.yaml

```
$ ls modules/
cars.py
$ cat evalgen.yaml
module_paths:
  - modules
```

Now you can run the apply spec
```
$ evalgen apply-spec --spec-class cars --loader-param DBURL  --output-file eval-dataset.jsonl
Data successfully transformed and saved to eval-dataset.jsonl
$ head eval-dataset.jsonl
{"Year":2009.0,"City mpg":27.0,"Highway mpg":37.5}
{"Year":2009.0,"City mpg":33.0,"Highway mpg":42.0}
{"Year":2009.0,"City mpg":31.5,"Highway mpg":45.0}
{"Year":2009.0,"City mpg":31.5,"Highway mpg":42.0}
...
```

## Setup

Set up environment:

1. Create a .env file in the project root
   a. Add DB_URL=your_database_url_here to the file
   b. Add OPENAI_API_KEY=your_openai_api_key_here to the file
b. evalgen.yaml in the local directory
    ```yaml
    module_paths:
      - /path/to/your/modules
      - /another/path/to/modules
    ```

    These modifications include the new functionality for loading subclasses of `Specification` and generating a sample YAML configuration.

## Todo

1. Test multiple sources
2. Specification templates
3. Test API usage