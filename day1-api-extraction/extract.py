"""
Day 1 - API Data Extraction and Transformation
Squad Python Specialization - Data Engineering

Fill in every function. Keep the signatures; you may add helpers of your own.
"""

import csv
import json
from pathlib import Path
import sys

import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = Path("output") / "customers_clean.csv"


def fetch_users(url: str = API_URL, timeout: float = 10.0) -> list[dict]:
    """Retrieve the list of users from the API.

    Must raise or report a clear error for: connection failures, timeouts,
    non-200 status codes and bodies that are not valid JSON.
    """
    # Use try-except block to catch any errors
    try:
        response = requests.get(url, timeout=timeout)

        # Check for the non-200 status codes
        if response.status_code != 200:
            print(f"Error: API returned a non-200 status code: {response.status_code}")
            sys.exit(1)

        # Parse JSON data
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: Not a valid JSON response.")
            sys.exit(1)

    # Report clear error for timeouts
    except requests.exceptions.Timeout:
        print(f"Error: The request timed out after {timeout} seconds.")
        sys.exit(1)

    # Report clear error for connection failures
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the API. Check your internet or URL")
        sys.exit(1)


def describe_structure(payload) -> None:
    """Print what Python types, the payload and one record are made of
    (the top-level container, a record, and each nested value)."""
    print("----------Data Structure Description-------------")
    print(f"Payload type: {type(payload).__name__}")

    # Ensure payload is a list
    if not payload or not isinstance(payload, list):
        print("Payload is empty or not a list.")
        return 

    # Check record types
    record = payload[0]
    print(f"Record type: {type(record).__name__}")
    print("Nested fields in a record:")

    # Use for loop to print out individual records
    for key, value in record.items():
        if isinstance(value, dict):
            print(f" - {key}: dict(depth 1)")
            for nested_key, nested_value in value.items():
                if isinstance(nested_value, dict):
                    print(f"    - {nested_key}: dict(depth 2)")
                else:
                    print(f"    - {nested_key}: {type(nested_value).__name__}")
        else:
            print(f" - {key}: {type(value).__name__}")
    print()   


def extract_core_fields(users: list[dict]) -> list[dict]:
    """Return one small dict per user with id, name, email, city and company name."""
    # create empty list
    extracted = []
    for user in users:
        # Use .get() to prevent errors on missing keys and extract nested data with defaults
        city = user.get("address", {}).get("city", "Unkown")
        company = user.get("company", {}).get("name", "Unknown")

        # Append user details to empty list
        extracted.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": city,
            "company": company
        })

    # Return list of extracted values
    return extracted 


def build_structures(users: list[dict]) -> tuple[list, list[tuple], dict]:
    """Return (list_of_names, list_of_(id, email)_tuples, dict_of_id_to_city).

    Use at least one list comprehension and one dict comprehension.
    """
    # List comprehension of names
    names = [user.get("name") for user in users]

    # List comprehension of tuples(id, email)
    id_email_tuples = [(user.get("id"), user.get("email")) for user in users]

    # Dict comprehension for id_to_city
    id_to_city = {}
    for user in users:
        user_id = user.get("id")
        city = user.get("address", {}).get("city", "Unknown")
        id_to_city[user_id] = city

    # Return names, id_email_tuples and id_to_city values
    return names, id_email_tuples, id_to_city


def flatten_user(user: dict, parent_key: str = "", sep: str = "_") -> dict:
    # Initialize an empty items list that'll contain the dictionaries
    items = []
    for key, value in user.items():
        # Force key to lowercase to match expected CSV headers
        key = key.lower() 
        # Rename nested dict key
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        
        if isinstance(value, dict):
            # Flatten nested dictionaries recursively
            items.extend(flatten_user(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def to_dataframe(flat_users: list[dict]) -> pd.DataFrame:
    """Build a DataFrame with the columns in the expected-output order."""
    df = pd.DataFrame(flat_users)
    
    # Rename id to customer_id
    if "id" in df.columns:
        df = df.rename(columns={"id": "customer_id"})
        
    # Convert coordinates to floats
    if "address_geo_lat" in df.columns:
        df["address_geo_lat"] = pd.to_numeric(df["address_geo_lat"], errors="coerce")
    if "address_geo_lng" in df.columns:
        df["address_geo_lng"] = pd.to_numeric(df["address_geo_lng"], errors="coerce")
        
    # List column order based on expected output
    expected_cols = [
        "customer_id", "name", "username", "email", "phone", "website",
        "address_street", "address_suite", "address_city", "address_zipcode",
        "address_geo_lat", "address_geo_lng", "company_name", "company_catchphrase", "company_bs"
    ]
    
    # Keep only the expected columns and reorder them
    df = df[[col for col in expected_cols if col in df.columns]]
    return df

def export_csv(df: pd.DataFrame, path: Path = OUTPUT_PATH) -> Path:
    """Write the DataFrame to CSV (creating the folder if needed) and return the path."""
    # create output directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # write data to CSV
    df.to_csv(path, index=False)
    return path


def main() -> None:
    # TODO: wire the steps together and print a short run summary.
    # Show starter script
    print("Starting API data extraction...")

    #Fetch data from API
    print(f"Fetching data from {API_URL}...")
    users = fetch_users()
    print(f"Fetched data successfully. Fetched {len(users)} records.")

    # Describe structure of extracted data
    describe_structure(users)

    # Extract core fields
    core_fields = extract_core_fields(users)
    print("----------Core Fields----------------")
    print(f"{len(core_fields)} users extracted.")
    print()

    # Build structures
    names, tuples, city_dict = build_structures(users)
    print("-------Structuring Data Demo-----------")
    print(f"First 5 names: {names[:5]}")
    print(f"First 5 (id, email) tuples: {tuples[:5]}")
    print(f"ID -> City mapping: {list(city_dict.items())[:5]}")
    print()
    
    # Flatten all records
    flat_users = [flatten_user(user) for user in users]
    print("-----------Flattened Users---------------")
    print(f"{len(flat_users)} records flattened.")
    print()

    # Load DataFrame and print df info
    df = to_dataframe(flat_users=flat_users)
    print("---------DataFrame info-------------")
    print(f"Shape: {df.shape}")
    print("Data Types:")
    print(df.dtypes)

    # Export to CSV
    saved_data_path = export_csv(df)
    print(f"\nCleaned data exported to: {saved_data_path}")


if __name__ == "__main__":
    main()