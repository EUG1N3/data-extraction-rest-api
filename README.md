# Data Extraction REST API: Python ETL Pipeline

## Overview

This project demonstrates how to build a Python-based data extraction and transformation pipeline that retrieves data from a REST API, inspects the JSON response, extracts relevant fields, flattens nested JSON structures, transforms the data into a tabular format, and exports the cleaned dataset to a CSV file.

The project uses the [JSONPlaceholder API](https://jsonplaceholder.typicode.com/users) as a sample data source.

It demonstrates fundamental data engineering concepts, including API integration, JSON processing, data transformation, error handling, and file-based data storage.

## Objectives

- Extract data from a REST API using Python.
- Handle HTTP responses and common API request errors.
- Inspect JSON payloads and understand nested data structures.
- Extract selected fields from JSON records.
- Work with Python lists, tuples, dictionaries, and list comprehensions.
- Flatten nested JSON objects into tabular records.
- Transform and organize data using Pandas.
- Export the transformed dataset to CSV.
- Apply Git version control and dependency management practices.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Requests | Sending HTTP requests to the REST API |
| Pandas | Data transformation and tabular data handling |
| JSON | Processing structured API responses |
| CSV | Exporting the transformed dataset |
| pathlib | Managing file paths |
| Git and GitHub | Version control and project hosting |
| VS Code | Development environment |

## Project Structure

```text
data-extraction-rest-api/
├── .gitignore
├── README.md
├── requirements.txt
├── .venv/
├── day1-api-extraction/
│   └── extract.py
└── output/
    └── customers_clean.csv
```

**Note:** `.venv/` and `output/` may be excluded from Git using `.gitignore`. The CSV file is generated when the pipeline runs, so it does not need to be committed unless you want to publish the sample output.

## Data Source

The project retrieves sample user records from:

`https://jsonplaceholder.typicode.com/users`

The API returns JSON records containing user information, including:

- User ID
- Name
- Username
- Email
- Address
- Geographic coordinates
- Phone number
- Website
- Company information

Some fields, such as `address`, `geo`, and `company`, are nested JSON objects. The pipeline transforms these nested structures into columns suitable for tabular analysis.

## Pipeline Workflow

The pipeline follows these steps:

1. **Data extraction:** Send an HTTP GET request to the API endpoint using Requests.
2. **Response validation:** Check the HTTP response and handle request failures.
3. **Structure inspection:** Examine the JSON payload and identify nested fields.
4. **Field extraction:** Select relevant attributes from each user record.
5. **Data structure operations:** Demonstrate lists, tuples, dictionaries, and list comprehensions.
6. **JSON flattening:** Convert nested JSON objects into flat dictionaries.
7. **Data transformation:** Load the flattened records into a Pandas DataFrame, rename selected columns, and convert geographic coordinates to numeric values.
8. **Data export:** Save the transformed data to `output/customers_clean.csv`.

## Prerequisites

Before running the project, ensure you have:

- Python 3.10 or later recommended.
- Git installed.
- Visual Studio Code or another Python-compatible editor.
- An internet connection to access the API.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/EUG1N3/data-extraction-rest-api.git
cd data-extraction-rest-api
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

When activated, your terminal should display `(.venv)`.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `requirements.txt` file should include the external packages required by the project, such as:

```text
pandas
requests
```

The Python standard-library modules, including `csv`, `json`, `pathlib`, and `sys`, do not need to be installed separately.

## Running the Pipeline

From the project root, execute:

```powershell
python day1-api-extraction/extract.py
```

The script should retrieve the API records, process the data, and generate the output CSV file.

If your script uses a relative output path, run it from the project root so that the output directory is created in the expected location.

## Expected Output

The pipeline produces a CSV file at:

`output/customers_clean.csv`

The resulting dataset is designed to contain flattened columns such as:

- `customer_id`
- `name`
- `username`
- `email`
- `phone`
- `website`
- `address_street`
- `address_suite`
- `address_city`
- `address_zipcode`
- `address_geo_lat`
- `address_geo_lng`
- `company_name`
- `company_catchphrase`
- `company_bs`

The output schema depends on the transformations implemented in the Python script.

## Error Handling

The extraction workflow is designed to handle common issues, including:

- HTTP errors or unsuccessful responses.
- Request timeouts.
- Connection errors.
- Invalid JSON responses.

These checks help make API extraction more reliable and make failures easier to diagnose.

## Key Learning Outcomes

By completing this project, you can demonstrate an understanding of:

- REST API integration with Python.
- JSON payload inspection and nested data extraction.
- Python data structures and comprehensions.
- Recursive dictionary flattening.
- Pandas DataFrame creation and column transformation.
- CSV file generation.
- Virtual environments and dependency management.
- Git version control and GitHub repository workflows.

## Future Improvements

Potential enhancements include:

- Add automated tests using `pytest`.
- Replace print-based error reporting with Python's `logging` module.
- Add retry logic and exponential backoff for transient API failures.
- Validate incoming records before transformation.
- Support pagination and incremental extraction for APIs that provide those features.
- Add configuration through environment variables.
- Load the transformed dataset into a data warehouse such as BigQuery or Snowflake.
- Automate execution through a scheduled workflow or CI/CD pipeline.

## Author

**Eugine**

Data Analyst & Analytics Engineer

This project is part of an ongoing journey in Python, data extraction, transformation, and analytics engineering.

## License

This project is intended for educational and portfolio purposes. Add a specific open-source license if you intend to permit others to reuse or distribute the code under defined terms.

