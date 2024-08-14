import os
import importlib
from typing import Optional
from sstc_core.sites.spectral import utils, sftp_tools
from sstc_core.sites.spectral.utils import normalize_string
from sstc_core.sites.spectral.io_tools import load_yaml 
from pathlib import Path
import duckdb
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Union
from sstc_core.sites.spectral.image_quality import assess_image_quality, calculate_normalized_quality_index, load_weights_from_yaml
from sstc_core.sites.spectral.data_products.qflags import compute_qflag
from sstc_core.sites.spectral.data_products import phenocams


class DatabaseError(Exception):
    """Base class for other exceptions"""
    pass

class RecordExistsError(DatabaseError):
    """Raised when the record already exists in the database"""
    pass

class RecordNotFoundError(DatabaseError):
    """Raised when the record is not found in the database"""
    pass



def generate_query_dict() -> Dict[str, Dict[str, Union[str, tuple]]]:
    """
    Generates a dictionary containing SQL query templates and their associated parameters.

    This function provides a centralized way to manage SQL queries and the parameters needed for
    each query. The keys of the dictionary represent the operation type, and each value is a dictionary
    containing the query template and a tuple of parameter names that are used in the query.

    Returns:
        Dict[str, Dict[str, Union[str, tuple]]]: A dictionary where each key is a string representing
        the operation (e.g., 'create_table', 'insert_record') and each value is another dictionary with:
            - 'query': The SQL query template as a string, where placeholders are used for dynamic values.
            - 'params': A tuple containing the names of the parameters expected for the query.
            
    Examples:
    
        ```python
        
        queries_dict = generate_query_dict()
        
        # Creating a table
        def create_table_example(db_manager, table_name: str, schema: str):
            query_info = queries_dict["create_table"]
            query = query_info["query"].format(table_name=table_name, schema=schema)
            db_manager.execute_query(query)

        ## Usage
        db_manager = DuckDBManager("example.db")
        create_table_example(db_manager, "users", "id INTEGER PRIMARY KEY, name TEXT")
        db_manager.close()
        
        # Inserting a record
        def insert_record_example(db_manager, table_name: str, record_dict: Dict[str, Any]):
            columns = ', '.join(record_dict.keys())
            placeholders = ', '.join(['?'] * len(record_dict))
            query_info = queries_dict["insert_record"]
            query = query_info["query"].format(table_name=table_name, columns=columns, placeholders=placeholders)
            db_manager.execute_query(query, tuple(record_dict.values()))

        ## Usage
        db_manager = DuckDBManager("example.db")
        record = {"id": 1, "name": "Alice"}
        insert_record_example(db_manager, "users", record)
        db_manager.close()
        
        # Fetching records
        def fetch_records_example(db_manager, table_name: str, condition: str):
            query_info = queries_dict["fetch_records"]
            query = query_info["query"].format(table_name=table_name, condition=condition)
            return db_manager.execute_query(query)

        ## Usage
        db_manager = DuckDBManager("example.db")
        records = fetch_records_example(db_manager, "users", "id = 1")
        print(records)  # Output: [(1, 'Alice')]
        db_manager.close()

        ``` 
    """
    queries = {
        "record_exists":{
            "query": "SELECT COUNT(*) FROM {table_name} WHERE catalog_guid ={catalog_guid}",
            "params": ("table_name", "catalog_guid"),
            
        }, 
        "create_table": {
            "query": "CREATE TABLE IF NOT EXISTS {table_name} ({schema});",
            "params": ("table_name", "schema"),
        },
        "record_exists": {
            "query": "SELECT 1 FROM {table_name} WHERE record_id = ? LIMIT 1",
            "params": ("table_name", "record_id"),
        },
        "insert_record": {
            "query": "INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            "params": ("table_name", "record_dict"),
        },
        "insert_multiple_records": {
            "query": "INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            "params": ("table_name", "records"),
        },
        "update_record": {
            "query": "UPDATE {table_name} SET {set_clause} WHERE {condition}",
            "params": ("table_name", "update_values", "condition"),
        },
        "delete_record": {
            "query": "DELETE FROM {table_name} WHERE {condition}",
            "params": ("table_name", "condition"),
        },
        "fetch_records": {
            "query": "SELECT * FROM {table_name} WHERE {condition}",
            "params": ("table_name", "condition"),
        },
        "fetch_by_year": {
            "query": "SELECT * FROM {table_name} WHERE year = ?",
            "params": ("table_name", "year"),
        },
        "fetch_by_is_selected": {
            "query": "SELECT * FROM {table_name} WHERE is_selected = ?",
            "params": ("table_name", "is_selected"),
        },
        "fetch_by_year_and_is_selected": {
            "query": "SELECT * FROM {table_name} WHERE year = ? AND is_selected = ?",
            "params": ("table_name", "year", "is_selected"),
        },
        "list_tables": {
            "query": "SHOW TABLES",
            "params": (),
        },
        "get_catalog_filepaths": {
            "query": "SELECT creation_date, catalog_filepath FROM {table_name} WHERE year(creation_date) = ?",
            "params": ("table_name", "year"),
        },
        "get_source_filepaths": {
            "query": "SELECT creation_date, source_filepath FROM {table_name} WHERE year(creation_date) = ?",
            "params": ("table_name", "year"),
        },
        "add_day_of_year_column": {
            "query": "ALTER TABLE {table_name} ADD COLUMN day_of_year INTEGER;",
            "params": ("table_name",),
        },
        "filter_by_time_window": {
            "query": "SELECT rowid, creation_date FROM {table_name}",
            "params": ("table_name",),
        },
        "populate_L0_name": {
            "query": "ALTER TABLE {table_name} ADD COLUMN L0_name TEXT;",
            "params": ("table_name",),
        },
        "check_is_L1": {
            "query": "ALTER TABLE {table_name} ADD COLUMN is_L1 BOOLEAN;",
            "params": ("table_name",),
        },
        "get_catalog_filepaths_by_year_and_day": {
            "query": "SELECT creation_date, day_of_year, L0_name, is_L1, location_id, platform_id, station_acronym, catalog_filepath, is_selected FROM {table_name}",
            "params": ("table_name", "year", "is_L1", "is_selected"),
        }
    }
    return queries


def generate_unique_id(creation_date: str, station_acronym: str, location_id: str, platform_id: str) -> str:
    """
    Generates a unique global identifier based on creation_date, station_acronym, location_id, and platform_id.

    Parameters:
        creation_date (str): The creation date of the record.
        station_acronym (str): The station acronym.
        location_id (str): The location ID.
        platform_id (str): The platform ID.

    Returns:
        str: A unique global identifier as a SHA-256 hash string.
    """
    # Concatenate the input values to form a unique string
    unique_string = f"{creation_date}_{station_acronym}_{location_id}_{platform_id}"
    
    # Generate the SHA-256 hash of the unique string
    unique_id = hashlib.sha256(unique_string.encode()).hexdigest()
    
    return unique_id


def get_stations_names_dict(yaml_filename: str = 'stations_names.yaml') -> Dict[str, Dict[str, str]]:
    """
    Retrieve a dictionary of station names with their respective system names and acronyms.

    Parameters:
        yaml_filename (str): The filename of the YAML file containing station information.

    Returns:
        dict: A dictionary where each key is a station name and the value is another dictionary
              containing the system name and acronym for the station.

    Raises:
        FileNotFoundError: If the YAML file is not found in the expected directory.
        yaml.YAMLError: If there is an error parsing the YAML file.

    Example:
        ```python
        get_stations_names_dict()
        {
            'Abisko': {'normalized_station_name': 'abisko', 'station_acronym': 'ANS', 'station_name': 'Abisko'}
            'Asa': {'normalized_station_name': 'asa', 'station_acronym': 'ASA', 'station_name': 'Asa'}
            'Grimsö': {'normalized_station_name': 'grimso', 'station_acronym': 'GRI', 'station_name': 'Grimsö'}
            'Lonnstorp': {'normalized_station_name': 'lonnstorp', 'station_acronym': 'LON', 'station_name': 'Lonnstorp'}
            'Robacksdalen': {'normalized_station_name': 'robacksdalen', 'station_acronym': 'RBD', 'station_name': 'Robacksdalen'}
            'Skogaryd': {'normalized_station_name': 'skogaryd', 'station_acronym': 'SKC', 'station_name': 'Skogaryd'}
            'Svartberget': {'normalized_station_name': 'svartberget', 'station_acronym': 'SVB', 'station_name': 'Svartberget'}
        }
        ```
    """
    # Get the parent directory of the current file
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dirpath = os.path.join(parent_directory, 'config')
    yaml_filepath = os.path.join(config_dirpath, yaml_filename)

    if not os.path.exists(yaml_filepath):
        raise FileNotFoundError(f"The file '{yaml_filepath}' does not exist.")

    try:
        data = load_yaml(yaml_filepath)        
        
    except Exception as e:
        raise ValueError(f"Error parsing YAML file: {e}")
    
    return data
    

class DuckDBManager:
    """
    A base class for managing DuckDB database connections and operations.
    """
    def __init__(self, db_filepath: str):
        """
        Initializes the DuckDBManager with the path to the database.

        Parameters:
        db_filepath (str): The file path to the DuckDB database.
        """
        self.db_filepath = db_filepath
        self.connection = None
        self.validate_db_filepath()
        self.close_connection()  # Close any existing connections on initialization

    def validate_db_filepath(self):
        """
        Validates the existence of the database file path.

        Raises:
        FileNotFoundError: If the database file does not exist at the specified path.
        """
        if not Path(self.db_filepath).is_file():
            raise FileNotFoundError(f"The database file '{self.db_filepath}' does not exist. "
                                    f"Please provide a valid database file path.")

    def connect(self):
        """
        Establishes a connection to the DuckDB database if not already connected.

        Raises:
            duckdb.Error: If there is an error connecting to the database.
        """
        if self.connection is None:
            try:
                self.connection = duckdb.connect(self.db_filepath)
            except duckdb.Error as e:
                raise duckdb.Error(f"Failed to connect to the DuckDB database: {e}")

    def execute_query(self, query: str, params: tuple = None):
        """
        Executes a SQL query on the DuckDB database.

        Parameters:
        query (str): The SQL query to execute.
        params (tuple, optional): A tuple of parameters to pass to the query.

        Returns:
        list: The result of the query as a list of tuples.

        Raises:
        duckdb.Error: If there is an error executing the query.
        """
        try:
            if self.connection is None:
                self.connect()
            if params:
                return self.connection.execute(query, params).fetchall()
            return self.connection.execute(query).fetchall()
        except duckdb.Error as e:
            raise duckdb.Error(f"Failed to execute query: {query}. Error: {e}")

    def close_connection(self):
        """
        Closes the connection to the DuckDB database if it is open.
        """
        if self.connection is not None:
            try:
                self.connection.close()
                print("DuckDB connection closed successfully.")
            except duckdb.Error as e:
                print(f"Failed to close the DuckDB connection: {e}")
            finally:
                self.connection = None

    def get_record_count(self, table_name: str) -> int:
        """
        Returns the number of records in the specified table.

        This method ensures that the DuckDB connection is open before executing the query.
        It will reopen the connection if it was closed.

        Parameters:
            table_name (str): The name of the table to count records in.

        Returns:
            int: The number of records in the table.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        
        try:
            if self.connection is None:
                self.connect()
                
            result = self.execute_query(query)
            return result[0][0]
        
        except duckdb.Error as e:
            print(f"An error occurred while getting the record count for table '{table_name}': {e}")
            raise

        finally:
            self.close_connection()
            
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Retrieves the schema of the specified table.

        This method returns the schema information for a given table, including column names, data types, and other attributes.

        Parameters:
            table_name (str): The name of the table for which to retrieve the schema.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a column in the table.
                                  The dictionary includes the column name, data type, and other properties.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        query = f"PRAGMA table_info('{table_name}')"
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query)
            schema_info = []

            for row in result:
                column_info = {
                    "column_id": row[0],
                    "column_name": row[1],
                    "data_type": row[2],
                    "not_null": bool(row[3]),
                    "default_value": row[4],
                    "primary_key": bool(row[5])
                }
                schema_info.append(column_info)

            return schema_info
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving the schema for table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()
            
    def get_filtered_records(self, table_name: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Returns a list of records as dictionaries, filtered by specified field-value pairs.

        Parameters:
            table_name (str): The name of the table to query.
            filters (Dict[str, Any]): A dictionary of field-value pairs to filter the records by.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a record with all fields included.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
            
        Example:
            ```python
            # Assuming you have an instance of Station
            station = Station(db_dirpath="/path/to/db/dir", station_name="StationName")

            # Define the filters for the query
            filters = {
                "is_L1": True,
                "year": 2024
            }

            # Retrieve the filtered records
            filtered_records = station.get_filtered_records(table_name="PhenoCams_BTH_FOR_P_BTH_1", filters=filters)
            for record in filtered_records:
                print(record)
            ```
        """
        try:
            if self.connection is None:
                self.connect()

            # Build the WHERE clause based on the filters
            where_clauses = []
            params = []
            for field, value in filters.items():
                where_clauses.append(f"{field} = ?")
                params.append(value)

            where_clause = " AND ".join(where_clauses)
            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            
            # Execute query and get the column names
            result = self.execute_query(query, tuple(params))
            columns = self.connection.execute(f"DESCRIBE {table_name}").fetchall()

            column_names = [col[0] for col in columns]
            
            records_list = []
            for row in result:
                # Convert tuple to dictionary using column names
                record_dict = dict(zip(column_names, row))
                records_list.append(record_dict)

            return records_list
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving records from table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()

    def update_record_by_catalog_guid(self, table_name: str, catalog_guid: str, updates: Dict[str, Any]) -> bool:
        """
        Updates the specified fields for a record identified by `catalog_guid`.

        Parameters:
            table_name (str): The name of the table where the record exists.
            catalog_guid (str): The unique identifier for the record.
            updates (Dict[str, Any]): A dictionary containing the fields and their new values to update.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            ValueError: If the record with the specified catalog_guid does not exist.
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        try:
            # Check if the record exists
            if not self.catalog_guid_exists(table_name, catalog_guid):
                raise ValueError(f"Record with catalog_guid {catalog_guid} does not exist in {table_name}.")

            # Build the SET clause dynamically from the updates dictionary
            set_clauses = []
            params = []
            for field, value in updates.items():
                set_clauses.append(f"{field} = ?")
                params.append(value)
            params.append(catalog_guid)

            set_clause = ", ".join(set_clauses)
            query = f"UPDATE {table_name} SET {set_clause} WHERE catalog_guid = ?"
            
            # Execute the update query
            self.execute_query(query, tuple(params))
            print(f"Successfully updated record with catalog_guid {catalog_guid}")
            return True

        except duckdb.Error as e:
            print(f"An error occurred while updating record with catalog_guid {catalog_guid}: {e}")
            return False

        finally:
            self.close_connection()
            
class Station(DuckDBManager):
    def __init__(self, db_dirpath: str, station_name: str):
        """
        Initializes the Station class with the directory path of the database and the station name.

        The database file is named using the normalized station name. If the file does not exist, a new
        database is created.

        Parameters:
            db_dirpath (str): The directory path where the DuckDB database is located.
            station_name (str): The name of the station.
        """
        self.station_name = station_name
        self.normalized_station_name = self.normalize_string(station_name)
        self.station_module = self._load_station_module()
        self.meta = getattr(self.station_module, 'meta', {})
        self.locations = getattr(self.station_module, 'locations', {})
        self.platforms = getattr(self.station_module, 'platforms', {})
        self.db_dirpath = Path(db_dirpath)
        self.db_filepath = self.db_dirpath / f"{self.normalized_station_name}_catalog.db"
        self.phenocam_quality_weights_filepath = self.meta.get("phenocam_quality_weights_filepath", None)
        self.sftp_dirpath = f'/{self.normalized_station_name}/data/'
        
        # Ensure the database file is created before calling the parent constructor
        if not self.db_filepath.exists():
            self.create_new_database()
        
        super().__init__(str(self.db_filepath))

        # Close the connection after initialization
        self.close_connection()

    def _load_station_module(self):
        """
        Dynamically loads the specified station submodule.

        Returns:
            module: The loaded module.
        """
        module_path = f"sstc_core.sites.spectral.stations.{self.normalized_station_name}"
        try:
            return importlib.import_module(module_path)
        except ModuleNotFoundError:
            raise ImportError(f"Module '{module_path}' could not be found or imported.")

    def create_new_database(self):
        """
        Creates a new DuckDB database file at the specified db_filepath.
        """
        # This will create a new file if it doesn't exist
        connection = duckdb.connect(str(self.db_filepath))
        connection.close()

    def get_station_data(self, query: str, params: Optional[tuple] = None):
        """
        Retrieves data from the station database based on a SQL query.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass with the query.

        Returns:
            Any: The result of the query execution.
        """
        return self.execute_query(query, params)

    def add_station_data(self, table_name: str, data: Dict[str, Any]):
        """
        Adds data to the specified table in the station database. Creates the table if it does not exist.

        Parameters:
            table_name (str): The name of the table to insert data into.
            data (Dict[str, Any]): The data to insert as a dictionary.
        """
        if not self.table_exists(table_name):
            self.create_table(table_name, data)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the station database.

        Parameters:
            table_name (str): The name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?"
        result = self.execute_query(query, (table_name,))
        return result[0][0] > 0

    def create_table(self, table_name: str, schema: Dict[str, str]):
        """
        Creates a new table in the station database with the schema based on the provided field names and types.

        Parameters:
            table_name (str): The name of the table to create.
            schema (Dict[str, str]): A dictionary where keys are field names and values are field types (e.g., 'INTEGER', 'DOUBLE', 'BOOLEAN', 'VARCHAR').

        Raises:
            ValueError: If a field type is not one of the supported types.
            
        Example:
            ```python
            # Assuming you have an instance of Station
            station = Station(db_dirpath="/path/to/db/dir", station_name="StationName")

            # Define the schema for the new table
            schema = {
                'catalog_guid': 'VARCHAR',
                'year': 'INTEGER',
                'creation_date': 'VARCHAR',
                'day_of_year': 'VARCHAR',
                'station_acronym': 'VARCHAR',
                'location_id': 'VARCHAR',
                'platform_id': 'VARCHAR',
                'ecosystem_of_interest': 'VARCHAR',
                'platform_type': 'VARCHAR',
                'is_legacy': 'BOOLEAN',
                'L0_name': 'VARCHAR',
                'is_L1': 'BOOLEAN',
                'is_ready_for_products_use': 'BOOLEAN',
                'catalog_filepath': 'VARCHAR',
                'source_filepath': 'VARCHAR',
                'normalized_quality_index': 'DOUBLE',
                'quality_index_weights_version': 'VARCHAR',
                'flags_confirmed': 'BOOLEAN'
            }

            # Create the new table with the specified schema
            table_name = "PhenoCams_BTH_FOR_P_BTH_1"
            station.create_table(table_name=table_name, schema=schema)
            ```        
        """
        # Supported field types
        valid_types = {'INTEGER', 'DOUBLE', 'BOOLEAN', 'VARCHAR'}
        
        columns = []
        for column_name, column_type in schema.items():
            if column_type not in valid_types:
                raise ValueError(f"Unsupported field type: {column_type}")
            columns.append(f"{column_name} {column_type}")
        
        columns_def = ', '.join(columns)
        query = f"CREATE TABLE {table_name} ({columns_def})"
        self.execute_query(query)


    def list_tables(self) -> List[str]:
        """
        Lists all tables in the station database.

        Returns:
            List[str]: A list of table names.
        """
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        result = self.execute_query(query)
        return [row[0] for row in result]

    def get_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the metadata of the station.

        Returns:
            dict: A dictionary with the station name as the key and a nested dictionary containing
                  db_filepath, meta, locations, and platforms as the value.
        """
        return {
            self.station_name: {
                "sftp_dirpath": str(self.sftp_dirpath),
                "db_filepath": str(self.db_filepath),
                "meta": self.meta,
                "locations": self.locations,
                "platforms": self.platforms
            }
        }
    
    def call_load_configurations(self) -> Any:
        """
        Calls `load_configurations` from the station submodule, if available.

        Returns:
            tuple: A tuple containing locations and platforms configuration data or None if the method does not exist.
        """
        load_configurations_method = getattr(self.station_module, 'load_configurations', None)
        if callable(load_configurations_method):
            return load_configurations_method()
        return None
    
    def catalog_guid_exists(self, table_name: str, catalog_guid: str) -> bool:
        """
        Checks if a record with the specified catalog_guid exists in the given table.

        Parameters:
            table_name (str): The name of the table to check.
            catalog_guid (str): The unique identifier to search for.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        query = f"SELECT COUNT(*) FROM {table_name} WHERE catalog_guid = ?"
        result = self.execute_query(query, (catalog_guid,))
        return result[0][0] > 0
    
    def insert_record(self, table_name: str, record_dict: Dict[str, Any]) -> bool:
        """
        Inserts a record into the specified table if the catalog_guid does not already exist.

        Parameters:
            table_name (str): The name of the table to insert the record into.
            record_dict (Dict[str, Any]): A dictionary representing the record to insert.

        Returns:
            bool: True if the record was inserted, False if it already existed.
        """
        catalog_guid = record_dict['catalog_guid']

        # Check if the catalog_guid already exists
        if self.catalog_guid_exists(table_name, catalog_guid):
            print(f"Record with catalog_guid {catalog_guid} already exists.")
            return False

        # Insert the record as it does not exist
        columns = ', '.join(record_dict.keys())
        placeholders = ', '.join(['?'] * len(record_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            self.execute_query(query, tuple(record_dict.values()))
            print(f"Inserted record with catalog_guid {catalog_guid}")
            return True
        except duckdb.Error as e:
            print(f"Error inserting record: {e}")
            return False
    
    def get_records_as_dictionary_by_day_L0_name(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> Dict[int, Dict[str, Dict[str, Any]]]:
        """
        Retrieves records filtered by specified criteria, structured in a nested dictionary format by day_of_year and L0_name.

        The dictionary structure is as follows:
        {
            day_of_year: {
                L0_name: {
                    'catalog_guid': ...,
                    'year': ...,
                    'creation_date': ...,
                    'day_of_year': ...,
                    'station_acronym': ...,
                    'location_id': ...,
                    'platform_id': ...,
                    'ecosystem_of_interest': ...,
                    'platform_type': ...,
                    'is_legacy': ...,
                    'L0_name': ...,
                    'is_L1': ...,
                    'is_ready_for_products_use': ...,
                    'catalog_filepath': ...,
                    'source_filepath': ...,
                    'normalized_quality_index': ...,
                    'quality_index_weights_version': ...,
                    'flag_brightness': ...,
                    'flag_blur': ...,
                    'flag_snow': ...,
                    'flag_rain': ...,
                    'flag_water_drops': ...,
                    'flag_dirt': ...,
                    'flag_obstructions': ...,
                    'flag_glare': ...,
                    'flag_fog': ...,
                    'flag_rotation': ...,
                    'flag_birds': ...,
                    'flag_other': ...,                    
                },
                ...
            },
            ...
        }

        Parameters:
            table_name (str): The name of the table to query.
            filters (Dict[str, Any], optional): Filters as a dictionary of field-value pairs. Defaults to None.

        Returns:
            Dict[int, Dict[str, Dict[str, Any]]]: A nested dictionary with `day_of_year` as the first key, 
                                                  `L0_name` as the second key, and all record fields as values.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        try:
            if self.connection is None:
                self.connect()

            # Build the WHERE clause based on the filters provided
            where_clauses = []
            params = []

            if filters:
                for field, value in filters.items():
                    where_clauses.append(f"{field} = ?")
                    params.append(value)

            where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            
            # Execute query and get the column names
            result = self.execute_query(query, tuple(params))
            columns = self.connection.execute(f"DESCRIBE {table_name}").fetchall()
            column_names = [col[0] for col in columns]
            
            records_by_day_L0_name = {}
            for row in result:
                # Convert tuple to dictionary using column names
                record_dict = dict(zip(column_names, row))
                
                day_of_year = record_dict['day_of_year']
                L0_name = record_dict['L0_name']

                if day_of_year not in records_by_day_L0_name:
                    records_by_day_L0_name[day_of_year] = {}
                
                records_by_day_L0_name[day_of_year][L0_name] = record_dict

            return records_by_day_L0_name
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving records from table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()        
            
    @staticmethod
    def normalize_string(name: str) -> str:
        """
        Normalizes a string by converting it to lowercase and replacing accented or non-English characters with their corresponding English characters.
        Specially handles Nordic characters. 
        
        
        Parameters:
            name (str): The string to normalize.

        Returns:
            str: The normalized string.
        
        Dependency:
            sstc_core.sites.spectral.utils.normalize_string
        
        """
        return utils.normalize_string(name)

    def phenocam_rois(self, platform_id: str, platforms_type: str = 'PhenoCams') -> dict:
        """
        Retrieves the Region of Interest (ROI) polygons for a specified PhenoCam platform.

        This method accesses the PhenoCam ROI polygons stored in a YAML-friendly format, deserializes them into a usable format,
        and returns the deserialized polygons.

        Parameters:
            platform_id (str): The identifier for the specific platform (e.g., 'P_BTH_1').
            platforms_type (str, optional): The type of platform. Defaults to 'PhenoCams'.

        Returns:
            dict: A dictionary containing the deserialized ROI polygons for the specified platform.

        Example:
            ```python
            # Assuming you have an instance of Station
            station = Station(db_dirpath="/path/to/db/dir", station_name="StationName")

            # Retrieve the PhenoCam ROIs for a specific platform
            platform_id = 'P_BTH_1'
            rois = station.phenocam_rois(platform_id=platform_id)

            print(rois)
            # Output might be a dictionary of ROI polygons, e.g.:
            # {'roi01': array([[100, 1800], [2700, 1550], [2500, 2700], [100, 2700]]), 
            #  'roi02': array([[100, 930], [3700, 1050], [3700, 1200], [100, 1400]])}
            ```

        Raises:
            KeyError: If the specified platform type or platform ID does not exist in the station's metadata, 
                    or if the ROI information is missing.
            ValueError: If the ROI data for the platform is empty or incorrectly formatted.

        Notes:
            - The method assumes that the ROIs are stored in a YAML-friendly format and requires deserialization using the `phenocams.deserialize_polygons` function.
            - The function `phenocams.deserialize_polygons` is assumed to be defined elsewhere and is responsible for converting the YAML-friendly format into a usable format.

        Dependencies:
            - This method depends on the `phenocams.deserialize_polygons` function to handle the deserialization of ROI polygons.
        """
        try:
            # Check if the platforms_type exists
            if platforms_type not in self.platforms:
                raise KeyError(f"The platform type '{platforms_type}' does not exist in the station's metadata.")

            # Check if the platform_id exists for the given platforms_type
            if platform_id not in self.platforms[platforms_type]:
                raise KeyError(f"The platform ID '{platform_id}' does not exist under platform type '{platforms_type}'.")

            # Retrieve the YAML-friendly ROI data
            yaml_friendly_rois = self.platforms[platforms_type][platform_id].get('phenocam_rois')
            
            if not yaml_friendly_rois:
                raise ValueError(f"No ROI data found for platform ID '{platform_id}' under platform type '{platforms_type}'.")

            # Deserialize the ROI data into a usable format
            phenocam_rois = phenocams.deserialize_polygons(
                yaml_friendly_rois=yaml_friendly_rois
            )   

            return phenocam_rois

        except KeyError as ke:
            print(f"KeyError: {ke}")
            raise

        except ValueError as ve:
            print(f"ValueError: {ve}")
            raise

        except Exception as e:
            print(f"An unexpected error occurred while retrieving PhenoCam ROIs: {e}")
            raise
        

    
    def create_record_dictionary(self, 
                                 remote_filepath: str, 
                                 platforms_type: str, 
                                 platform_id: str,
                                 processing_level_products_dict: dict = {'PhenoCams':{
                                     'L2_RGB_CIMV_filepath': None,
                                     'L2_GCC_CIMV_filepath': None,
                                     'L2_RCC_CIMV_filepath': None,
                                     'L2_RGB_CISDV_filepath': None,
                                     'L2_GCC_CISDV_filepath': None,
                                     'L2_RCC_CISDV_filepath': None,                                                                          
                                 }},
                                 is_legacy: bool = False, 
                                 backup_dirpath: str = 'aurora02_dirpath', 
                                 start_time: str = "10:00:00", 
                                 end_time: str = "14:30:00", 
                                 split_subdir: str = 'data', 
                                 skip: bool = False, 
                                 timezone_str: str ='Europe/Stockholm',
                                 has_snow_presence:bool = False,
                                 ) -> Dict[str, Any]:
        """
        Creates a dictionary representing a record for a file, including metadata and derived attributes.

        This method constructs a record dictionary for a given file located at `remote_filepath` on an SFTP server. 
        The record includes various metadata such as creation date, station acronym, location ID, platform type, 
        platform ID, whether the data is legacy, and a generated unique ID. The function also checks if the creation 
        time of the file falls within a specified time window and generates an L0 name for the file.

        Parameters:
            remote_filepath (str): The path to the remote file on the SFTP server.
            platforms_type (str): The type of platform (e.g., 'PhenoCams', 'UAVs', 'FixedSensors', 'Satellites').
            platform_id (str): The identifier for the specific platform.
            processing_level_products_dict (dict, optional): A dictionary containing processing level product fields. Defaults to {'PhenoCams': {...}}.
            is_legacy (bool, optional): Indicates whether the record is considered legacy data. Defaults to False.
            backup_dirpath (str, optional): The directory path used for backup storage in the local filesystem. Defaults to 'aurora02_dirpath'.
            start_time (str, optional): The start of the time window in 'HH:MM:SS' format. Defaults to "10:00:00".
            end_time (str, optional): The end of the time window in 'HH:MM:SS' format. Defaults to "14:30:00".
            split_subdir (str, optional): The subdirectory name used to organize local paths. Defaults to 'data'.
            skip (bool, optional): If True, do not auto-assess image quality, leaving default values. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the record information, including metadata, derived attributes, and a unique ID.

        Raises:
            Exception: If there are issues retrieving or processing the file data.
        """
        # Retrieve local directory path from the station's platform data
        local_dirpath = self.platforms[platforms_type][platform_id]['backups'][backup_dirpath]

        # Get local file path
        local_filepath = sftp_tools.get_local_filepath(
            local_dirpath=local_dirpath, 
            remote_filepath=remote_filepath,
            split_subdir=split_subdir
        )

        # Extract creation date and format it
        creation_date = utils.get_image_dates(local_filepath)
        formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
        normalized_date = creation_date.strftime('%Y%m%d%H%M%S')
        year = creation_date.year
        day_of_year = utils.get_day_of_year(formatted_date)
        
        latitude_dd = self.platforms[platforms_type][platform_id]['geolocation']['point']['latitude_dd']
        longitude_dd = self.platforms[platforms_type][platform_id]['geolocation']['point']['longitude_dd']
        
        # TODO: refactor to `utils.sun_illumination_conditions`
        sun_position = utils.calculate_sun_position(
                datetime_str= formatted_date, 
                latitude_dd=latitude_dd, 
                longitude_dd=longitude_dd, 
                timezone_str=timezone_str)
        
        sun_elevation_angle = sun_position['sun_elevation_angle']
        sun_azimuth_angle = sun_position['sun_azimuth_angle'] 
               
        solar_elevation_class = utils.get_solar_elevation_class(sun_elevation=sun_elevation_angle)


        # Extract station and platform information
        station_acronym = self.meta['station_acronym']
        location_id = self.platforms[platforms_type][platform_id]['location_id']
        ecosystem_of_interest = self.platforms[platforms_type][platform_id]['ecosystem_of_interest']
        platform_type = self.platforms[platforms_type][platform_id]['platform_type']

        # Generate L0 name
        L0_name = f'SITES-{station_acronym}-{location_id}-{platform_id}-DOY_{day_of_year}-{normalized_date}'

        # Determine if the record is L1 based on time window
        is_L1 = utils.is_within_time_window(
            formatted_date=formatted_date,
            start_time=start_time,
            end_time=end_time
        )
        
        # Assess image quality
        quality_flags_dict = assess_image_quality(local_filepath, flag_other=False, flag_birds=False, skip=skip)
        weights = load_weights_from_yaml(self.phenocam_quality_weights_filepath)
        normalized_quality_index, quality_index_weights_version = calculate_normalized_quality_index(
            quality_flags_dict=quality_flags_dict,
            weights=weights, 
            skip=skip
        )
        
        # 
        phenocams_rois_dict = self.phenocam_rois(platform_id=platform_id)
        rois_dict ={} 
        if phenocams_rois_dict:
            for r in phenocams_rois_dict.keys():
                rois_dict[f'L3_{r}_has_snow_presence'] = None
                rois_dict[f'L3_{r}_QFLAG'] = None
                rois_dict[f'L3_{r}_mean_value'] = None
                rois_dict[f'L3_{r}_standard_deviation_value'] = None
                rois_dict[f'L3_{r}_number_quality_images'] = None 
                  
                
        # Create the record dictionary
        record_dict = {
            'catalog_guid': None,
            'year': year,
            'creation_date': formatted_date,
            'day_of_year': day_of_year,
            'station_acronym': station_acronym,
            'location_id': location_id,
            'platform_id': platform_id,
            'ecosystem_of_interest': ecosystem_of_interest,
            'platform_type': platform_type,
            'is_legacy': is_legacy,
            'L0_name': L0_name,
            'is_L1': is_L1,            
            'is_ready_for_products_use': False,          
            'catalog_filepath': local_filepath,
            'source_filepath': remote_filepath,
            'normalized_quality_index': normalized_quality_index,
            'quality_index_weights_version': quality_index_weights_version,
            'flags_confirmed': False,
            'has_snow_presence': has_snow_presence,            
            'sun_elevation_angle': sun_elevation_angle,
            'sun_azimuth_angle': sun_azimuth_angle,
            'solar_elevation_class': solar_elevation_class,            
        }

        QFLAF = compute_qflag(
            latitude_dd=latitude_dd,
            longitude_dd=longitude_dd,
            records_dict=record_dict, 
            has_snow_presence=has_snow_presence,
            timezone_str=timezone_str            
            )
        
        # Merge with quality flags and processing level product fields
        record_dict = {
            **record_dict,
            **{'QFLAG_image': QFLAF},  
            **quality_flags_dict, 
            **processing_level_products_dict[platforms_type],
            **rois_dict} 
        
        # Generate a unique ID for the catalog
        record_dict['catalog_guid'] = utils.generate_unique_id(
            record_dict, 
            variable_names=['creation_date', 'station_acronym', 'location_id', 'platform_id']
        )

        return record_dict
    
        
    def populate_station_db(self, sftp_filepaths: list, platform_id: str, platforms_type: str = 'PhenoCams',
                            backup_dirpath: str = 'aurora02_dirpath', start_time: str = "10:00:00",
                            end_time: str = "14:30:00", split_subdir: str = 'data', skip:bool = False) -> bool:
        """
        Populates the station database with records based on SFTP file paths.

        This method iterates over a list of file paths from an SFTP server, creates record dictionaries,
        and inserts them into the station's DuckDB database. It checks if a record already exists based on the
        `catalog_guid` before insertion.

        Parameters:
            sftp_filepaths (list): A list of file paths on the SFTP server to process.
            platform_id (str): The identifier for the specific platform.
            platforms_type (str, optional): The type of platform (default is 'PhenoCams').
            backup_dirpath (str, optional): The directory path used for backup storage in the local filesystem.
            start_time (str, optional): The start of the time window in 'HH:MM:SS' format (default is "10:00:00").
            end_time (str, optional): The end of the time window in 'HH:MM:SS' format (default is "14:00:00").
            split_subdir (str, optional): The subdirectory name to split the file path on (default is 'data').
            skip (bool, optional): If True do not auto-assess image quality, leaving default values.
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            for remote_filepath in sftp_filepaths:
                # Create record dictionary for the given file
                record = self.create_record_dictionary(
                    remote_filepath=remote_filepath,
                    platforms_type=platforms_type,
                    platform_id=platform_id,
                    is_legacy=False,
                    backup_dirpath=backup_dirpath,
                    start_time=start_time,
                    end_time=end_time,
                    split_subdir=split_subdir,
                    skip=skip,
                )
                
                catalog_guid = record.get('catalog_guid')
                platform_type = record.get('platform_type')
                if not catalog_guid:
                    print(f"Failed to generate catalog_guid for file: {remote_filepath}")
                    continue

                # Define table name based on platform details
                table_name = f"{platform_type}_{record['location_id']}_{platform_id}"

                # Check if the record already exists
                if not self.catalog_guid_exists(table_name=table_name, catalog_guid=catalog_guid):
                    self.add_station_data(table_name=table_name, data=record)
                else:
                    print(f"Record with catalog_guid {catalog_guid} already exists in {table_name}.")
            return True

        except duckdb.Error as e:
            print(f"Error inserting record: {e}")
            return False

    def update_is_ready_for_products_use(self, table_name: str, catalog_guid: str, is_ready_for_products_use: bool):
        """
        Updates the `is_ready_for_products_use` field for a specific record identified by `catalog_guid`.

        Parameters:
            table_name (str): The name of the table to update the record in.
            catalog_guid (str): The unique identifier for the record.
            is_ready_for_products_use(bool): The new value for the `is_ready_for_products_use` field.

        Raises:
            ValueError: If the record with the specified catalog_guid does not exist.
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        try:
            # Check if the record exists
            if not self.catalog_guid_exists(table_name, catalog_guid):
                raise ValueError(f"Record with catalog_guid {catalog_guid} does not exist in {table_name}.")

            # Update the `is_ready_for_products_use`` field for the record
            query = f"UPDATE {table_name} SET is_ready_for_products_use = ? WHERE catalog_guid = ?"
            self.execute_query(query, (is_ready_for_products_use, catalog_guid))
            print(f"Updated `is_ready_for_products_use` for catalog_guid {catalog_guid} to {is_ready_for_products_use}")

        except duckdb.Error as e:
            print(f"An error occurred while updating is_quality_confirmed for catalog_guid {catalog_guid}: {e}")
            raise

        finally:
            self.close_connection()
            
    def get_unique_years(self, table_name: str) -> List[int]:
        """
        Retrieves all unique values from the 'year' field in the specified table.

        Parameters:
            table_name (str): The name of the table from which to retrieve unique years.

        Returns:
            List[int]: A list of unique years present in the table.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        query = f"SELECT DISTINCT year FROM {table_name} ORDER BY year"
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query)
            unique_years = [row[0] for row in result]

            return unique_years
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving unique years from table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()
            
    def get_day_of_year_min_max(self, table_name: str, year: int) -> Dict[str, int]:
        """
        Retrieves the minimum and maximum values of the `day_of_year` field for the given year.

        Parameters:
            table_name (str): The name of the table to query.
            year (int): The year to filter records by.

        Returns:
            Dict[str, int]: A dictionary containing the minimum and maximum values of the `day_of_year` field.
                            The dictionary has keys 'min' and 'max'.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        query = f"SELECT day_of_year FROM {table_name} WHERE year = ?"
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query, (year,))
            
            if not result:
                return {'min': None, 'max': None}

            # Convert the day_of_year strings to integers
            day_of_year_ints = [int(row[0]) for row in result]
            min_day_of_year = min(day_of_year_ints)
            max_day_of_year = max(day_of_year_ints)

            return {'min': min_day_of_year, 'max': max_day_of_year}
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving min and max day_of_year from table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()
            
    def get_records_by_year_and_day_of_year(self, table_name: str, year: int, day_of_year: str) -> Dict[str, Dict[str, Any]]:
        """
        Retrieves all records for a given year and day_of_year, structured in a dictionary by catalog_guid.

        The dictionary structure is as follows:
        {
            catalog_guid: {
                'catalog_guid': ...,
                'year': ...,
                'creation_date': ...,
                'day_of_year': ...,
                'station_acronym': ...,
                'location_id': ...,
                'platform_id': ...,
                'ecosystem_of_interest': ...,
                'platform_type': ...,
                'is_legacy': ...,
                'L0_name': ...,
                'is_L1': ...,
                'is_ready_for_products_use': ...,
                'catalog_filepath': ...,
                'source_filepath': ...,
                'normalized_quality_index': ...,
                'quality_index_weights_version': ...,
                'flag_brightness': ...,
                'flag_blur': ...,
                'flag_snow': ...,
                'flag_rain': ...,
                'flag_water_drops': ...,
                'flag_dirt': ...,
                'flag_obstructions': ...,
                'flag_glare': ...,
                'flag_fog': ...,
                'flag_rotation': ...,
                'flag_birds': ...,
                'flag_other': ...,
                ...
            },
            ...
        }

        Parameters:
            table_name (str): The name of the table to query.
            year (int): The year to filter records by.
            day_of_year (str): The day of year to filter records by (formatted as a 3-character string).

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary with `catalog_guid` as the key and all record fields as values.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        query = f"SELECT * FROM {table_name} WHERE year = ? AND day_of_year = ?"
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query, (year, day_of_year))
            columns = self.connection.execute(f"DESCRIBE {table_name}").fetchall()
            column_names = [col[0] for col in columns]
            
            records_by_catalog_guid = {}
            for row in result:
                # Convert tuple to dictionary using column names
                record_dict = dict(zip(column_names, row))
                
                catalog_guid = record_dict['catalog_guid']
                records_by_catalog_guid[catalog_guid] = record_dict

            return records_by_catalog_guid
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving records from table '{table_name}' for year {year} and day_of_year {day_of_year}: {e}")
            raise
        
        finally:
            self.close_connection()
    
    def add_new_fields_to_table(self, table_name: str, new_fields: List[Dict[str, Any]]) -> bool:
        """
        Adds new fields to an existing table and initializes them with default values for all records.

        Parameters:
            table_name (str): The name of the table to modify.
            new_fields (List[Dict[str, Any]]): A list of dictionaries where each dictionary contains:
                                               - 'field_name' (str): The name of the new field.
                                               - 'field_type' (str): The type of the new field (e.g., 'INTEGER', 'DOUBLE', 'BOOLEAN', 'VARCHAR').
                                               - 'field_default_value' (Any, optional): The default value for the new field. Defaults to None.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            ValueError: If the default value cannot be cast to the specified field type.
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        def cast_value(value, value_type):
            try:
                if value_type == 'INTEGER':
                    return int(value)
                elif value_type == 'DOUBLE':
                    return float(value)
                elif value_type == 'BOOLEAN':
                    return bool(value)
                elif value_type == 'VARCHAR':
                    return str(value)
                else:
                    raise ValueError(f"Unsupported field type: {value_type}")
            except ValueError as e:
                raise ValueError(f"Cannot cast value {value} to {value_type}: {e}")

        try:
            if self.connection is None:
                self.connect()

            for field in new_fields:
                field_name = field['field_name']
                field_type = field['field_type']
                field_default_value = field.get('field_default_value', None)

                # Ensure the field_default_value can be cast to the field_type
                if field_default_value is not None:
                    cast_value(field_default_value, field_type)
                else:
                    field_default_value = None

                # Add the new field to the table schema
                alter_query = f"ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type}"
                self.execute_query(alter_query)

                # Update the existing records to set the default value for the new field
                update_query = f"UPDATE {table_name} SET {field_name} = ?"
                self.execute_query(update_query, (field_default_value,))
            
            return True
        
        except (ValueError, duckdb.Error) as e:
            print(f"An error occurred while adding new fields to table '{table_name}': {e}")
            return False
        
        finally:
            self.close_connection()
            
            
    def get_records_ready_for_products_by_year(self, table_name: str, year: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        Retrieves records filtered by the specified year and is_ready_for_products_use = True,
        structured in a dictionary with day_of_year as the key and a list of record dictionaries as the values.

        The dictionary structure is as follows:
        {
            day_of_year: [
                {
                    'catalog_guid': ...,
                    'year': ...,
                    'creation_date': ...,
                    'day_of_year': ...,
                    'station_acronym': ...,
                    'location_id': ...,
                    'platform_id': ...,
                    'ecosystem_of_interest': ...,
                    'platform_type': ...,
                    'is_legacy': ...,
                    'L0_name': ...,
                    'is_L1': ...,
                    'is_ready_for_products_use': ...,
                    'catalog_filepath': ...,
                    'source_filepath': ...,
                    'normalized_quality_index': ...,
                    'quality_index_weights_version': ...,
                    'flag_brightness': ...,
                    'flag_blur': ...,
                    'flag_snow': ...,
                    'flag_rain': ...,
                    'flag_water_drops': ...,
                    'flag_dirt': ...,
                    'flag_obstructions': ...,
                    'flag_glare': ...,
                    'flag_fog': ...,
                    'flag_rotation': ...,
                    'flag_birds': ...,
                    'flag_other': ...,
                    'is_quality_assessed': ...,
                },
                ...
            ],
            ...
        }

        Parameters:
            table_name (str): The name of the table to query.
            year (int): The year to filter records by.

        Returns:
            Dict[int, List[Dict[str, Any]]]: A dictionary with day_of_year as the key and a list of record dictionaries as the values.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        query = f"SELECT * FROM {table_name} WHERE year = ? AND is_ready_for_products_use = TRUE"
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query, (year,))
            columns = self.connection.execute(f"DESCRIBE {table_name}").fetchall()
            column_names = [col[0] for col in columns]
            
            records_by_day_of_year = {}
            for row in result:
                # Convert tuple to dictionary using column names
                record_dict = dict(zip(column_names, row))
                
                day_of_year = int(record_dict['day_of_year'])

                if day_of_year not in records_by_day_of_year:
                    records_by_day_of_year[day_of_year] = []
                
                records_by_day_of_year[day_of_year].append(record_dict)

            return records_by_day_of_year
        
        except duckdb.Error as e:
            print(f"An error occurred while retrieving records from table '{table_name}' for year {year} and is_ready_for_products_use=True: {e}")
            raise
        
        finally:
            self.close_connection()
            
    def delete_fields_from_table(self, table_name: str, fields_to_delete: List[str]) -> bool:
        """
        Deletes fields from an existing table.

        Parameters:
            table_name (str): The name of the table to modify.
            fields_to_delete (List[str]): A list of field names to be deleted from the table.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
        """
        try:
            if self.connection is None:
                self.connect()

            for field_name in fields_to_delete:
                # Drop the field from the table schema
                alter_query = f"ALTER TABLE {table_name} DROP COLUMN {field_name}"
                self.execute_query(alter_query)
            
            return True
        
        except duckdb.Error as e:
            print(f"An error occurred while deleting fields from table '{table_name}': {e}")
            return False
        
        finally:
            self.close_connection()
            
    def select_random_record(self, table_name: str) -> Dict[str, Any]:
        """
        Selects a random record from the specified table.

        Parameters:
            table_name (str): The name of the table to select a random record from.

        Returns:
            Dict[str, Any]: A dictionary representing the randomly selected record.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
            ValueError: If the table is empty.
        """
        query = f"SELECT * FROM {table_name} USING SAMPLE 1"
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query)
            if not result:
                raise ValueError(f"The table '{table_name}' is empty.")

            record = result[0]
            columns_query = f"PRAGMA table_info({table_name})"
            columns_result = self.execute_query(columns_query)
            columns = [col[1] for col in columns_result]

            return dict(zip(columns, record))
        
        except (duckdb.Error, ValueError) as e:
            print(f"An error occurred while selecting a random record from table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()
            
    def get_time_interval(self, table_name: str, year: int, is_ready_for_products_use: bool = True, **filters) -> str:
        """
        Retrieves the minimum and maximum dates of the `creation_date` field for a given year and other optional filters.

        Parameters:
            table_name (str): The name of the table to query.
            year (int): The year to filter the records by.
            is_ready_for_products_use (bool): Filter for records that are ready for product use. Defaults to True.
            **filters: Additional filters as keyword arguments.

        Returns:
            str: A string representing the minimum and maximum dates in the format `YYYYMMDD-YYYYMMDD`.

        Raises:
            duckdb.Error: If there is an error executing the query or managing the connection.
            ValueError: If no records are found for the given filters.
        """
        query = f"""
        SELECT MIN(creation_date), MAX(creation_date)
        FROM {table_name}
        WHERE year = ? AND is_ready_for_products_use = ?
        """
        
        params = [year, is_ready_for_products_use]
        
        for key, value in filters.items():
            query += f" AND {key} = ?"
            params.append(value)
        
        try:
            if self.connection is None:
                self.connect()

            result = self.execute_query(query, tuple(params))
            if not result or result[0][0] is None or result[0][1] is None:
                raise ValueError(f"No records found for the given filters in table '{table_name}'.")

            min_date_str = result[0][0]
            max_date_str = result[0][1]

            min_date = datetime.strptime(min_date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
            max_date = datetime.strptime(max_date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')

            return f"{min_date}-{max_date}"
        
        except (duckdb.Error, ValueError) as e:
            print(f"An error occurred while retrieving min and max dates from table '{table_name}': {e}")
            raise
        
        finally:
            self.close_connection()
            

def get_station_platform_geolocation_point(station: Station, platforms_type: str, platform_id: str) -> tuple:
    """
    Retrieves the geolocation (latitude and longitude) of a specific platform for a given station.

    Parameters:
        station (Station): An instance of the Station class that contains metadata about the station and its platforms.
        platforms_type (str): The type of platform (e.g., 'PhenoCams', 'UAVs', 'FixedSensors', 'Satellites').
        platform_id (str): The identifier for the specific platform.

    Returns:
        tuple: A tuple containing the latitude and longitude of the platform in decimal degrees, in the format (latitude_dd, longitude_dd).

    Example:
        ```python
        # Assuming you have an instance of Station
        station = Station(db_dirpath="/path/to/db/dir", station_name="StationName")

        # Retrieve the geolocation for a specific platform
        platforms_type = 'PhenoCams'
        platform_id = 'P_BTH_1'
        latitude_dd, longitude_dd = get_station_platform_geolocation_point(station, platforms_type, platform_id)

        print(f"Latitude: {latitude_dd}, Longitude: {longitude_dd}")
        ```

    Raises:
        KeyError: If the specified platform type or platform ID does not exist in the station's metadata, or if the geolocation information is incomplete.

    Note:
        This function assumes that the geolocation information is available in the station's metadata under the specified platform type and platform ID. 
        The geolocation should be stored in the format:
            station.platforms[platforms_type][platform_id]['geolocation']['point']['latitude_dd']
            station.platforms[platforms_type][platform_id]['geolocation']['point']['longitude_dd']
    """
    latitude_dd = station.platforms[platforms_type][platform_id]['geolocation']['point']['latitude_dd']
    longitude_dd = station.platforms[platforms_type][platform_id]['geolocation']['point']['longitude_dd']
    return latitude_dd, longitude_dd
