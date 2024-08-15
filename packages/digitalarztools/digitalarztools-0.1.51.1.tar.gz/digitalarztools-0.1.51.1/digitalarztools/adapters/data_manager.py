import os
import sqlite3
import json
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame

from digitalarztools.io.file_io import FileIO


class DataManager:
    def __init__(self, folder_path: str, base_name: str, purpose: str = None):
        self.db_path = os.path.join(folder_path, f"da_{base_name}.db")
        FileIO.mkdirs(self.db_path)
        self.metadata_file = os.path.join(folder_path, f"da_{base_name}_metadata.json")
        self.metadata = {
            "field_name": [],
            "geom_field_name": "",
            "record_count": 0,
            "purpose": purpose,
            "additional_cols": []
        }
        self.table_name = "records"
        self._initialize_db()
        self._load_metadata()

    def _initialize_db(self):
        # Initialize the SQLite database and create the table if it doesn't exist
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE,
                data JSON,
                geom BLOB
            )
        ''')
        self.conn.commit()

    def _load_metadata(self):
        # Load metadata from the JSON file
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as file:
                self.metadata = json.load(file)

    def _save_metadata(self):
        # Save metadata to the JSON file
        with open(self.metadata_file, 'w') as file:
            json.dump(self.metadata, file, indent=4)

    def add_record(self, key: str, record: dict, geom=None):
        try:
            record_json = json.dumps(record)
            geom_wkb = sqlite3.Binary(geom) if geom is not None else None
            query = f'INSERT INTO {self.table_name} (key, data, geom) VALUES (?, ?, ?)'
            self.cursor.execute(query, (key, record_json, geom_wkb))
            self.metadata['field_name'] = list(record.keys())
            self.metadata['record_count'] += 1
            self.conn.commit()
            self._save_metadata()
            return True
        except sqlite3.IntegrityError:
            print(f"Record with key '{key}' already exists.")
            return False

    def update_record(self, key: str, record: dict, geom=None):
        record_json = json.dumps(record)
        geom_wkb = sqlite3.Binary(geom) if geom is not None else None
        query = f'UPDATE {self.table_name} SET data = ?, geom = ? WHERE key = ?'
        self.cursor.execute(query, (record_json, geom_wkb, key))
        if self.cursor.rowcount == 0:
            print(f"Record with key '{key}' does not exist.")
            return False
        self.conn.commit()
        return True

    def get_record(self, key: str):
        query = f'SELECT data, geom FROM {self.table_name} WHERE key = ?'
        self.cursor.execute(query, (key,))
        result = self.cursor.fetchone()
        if result:
            record = json.loads(result[0])
            geom = gpd.GeoSeries.from_wkb(result[1]) if result[1] is not None else None
            return record, geom
        return None, None

    def record_exists(self, key: str):
        query = f'SELECT 1 FROM {self.table_name} WHERE key = ?'
        self.cursor.execute(query, (key,))
        return self.cursor.fetchone() is not None

    def get_metadata(self):
        return self.metadata

    def get_data_as_df(self, query: str = None) -> pd.DataFrame:
        if query is None:
            # Prepare the list of columns to fetch
            columns_to_select = ['key', 'data']

            # Add additional columns from metadata to the selection list
            if "additional_cols" in self.metadata:
                columns_to_select.extend(self.metadata["additional_cols"])

            # Build the SQL query with the necessary columns
            columns_str = ', '.join(columns_to_select)
            query = f'SELECT {columns_str} FROM {self.table_name}'

        # Execute the query
        self.cursor.execute(query)

        # Fetch the data and get the column names from the query
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Process the fetched rows
        records = []
        for row in rows:
            record_dict = {}
            for col_name, col_value in zip(column_names, row):
                if isinstance(col_value, str):
                    try:
                        # Attempt to load JSON data
                        json_data = json.loads(col_value)
                        if isinstance(json_data, dict):
                            record_dict.update(json_data)  # Merge JSON data if it’s a dictionary
                        else:
                            record_dict[col_name] = json_data  # Add non-dict JSON data as-is
                    except json.JSONDecodeError:
                        record_dict[col_name] = col_value  # Add string as-is if not JSON
                else:
                    record_dict[col_name] = col_value  # Add other data types as they are
            records.append(record_dict)

        # Convert records to a DataFrame
        df = pd.DataFrame(records)
        return df

    def get_data_as_gdf(self, query: str = None) -> GeoDataFrame:
        if query is None:
            # Prepare the list of columns to fetch
            columns_to_select = ['key', 'data', 'geom']

            # Add additional columns from metadata to the selection list
            if "additional_cols" in self.metadata:
                columns_to_select.extend(self.metadata["additional_cols"])

            # Build the SQL query with the necessary columns
            columns_str = ', '.join(columns_to_select)
            query = f'SELECT {columns_str} FROM {self.table_name} WHERE geom IS NOT NULL'

        # Execute the query
        self.cursor.execute(query)

        # Fetch the data and get the column names from the query
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Process the fetched rows
        records = []
        geoms = []
        for row in rows:
            record_dict = {}
            geom = None
            for col_name, col_value in zip(column_names, row):
                if isinstance(col_value, bytes):
                    if col_name == 'geom':
                        geom = gpd.GeoSeries.from_wkb(col_value)  # Convert WKB to GeoSeries
                elif isinstance(col_value, str):
                    try:
                        # Attempt to load JSON data
                        json_data = json.loads(col_value)
                        if isinstance(json_data, dict):
                            record_dict.update(json_data)  # Merge JSON data if it’s a dictionary
                        else:
                            record_dict[col_name] = json_data  # Add non-dict JSON data as-is
                    except json.JSONDecodeError:
                        record_dict[col_name] = col_value  # Add string as-is if not JSON
                else:
                    record_dict[col_name] = col_value  # Add other data types as they are

            records.append(record_dict)
            geoms.append(geom)

        # Convert records to a DataFrame
        df = pd.DataFrame(records)

        # Create a GeoDataFrame with the geometry
        gdf = gpd.GeoDataFrame(df, geometry=geoms)
        return gdf

    def add_column(self, column_name: str, data_type: str, default_value=None):
        """
        Add a new column to the table if it doesn't already exist.

        @param column_name: Name of the new column.
        @param data_type: Type of the new column like
             TEXT, INTEGER, BLOB
             DATE (YYYY-MM-DD), TIME (hh:mm:ss) and TIMESTAMP (YYYY-MM-DD hh:mm:ss)
        @param default_value: Default value for the new column.
        """
        try:
            # Check if the column already exists
            self.cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns = [info[1] for info in self.cursor.fetchall()]
            if column_name in columns:
                print(f"Column '{column_name}' already exists. Skipping addition.")
                return

            # Construct the SQL statement for adding a new column with a default value
            sql = f'ALTER TABLE {self.table_name} ADD COLUMN {column_name} {data_type}'
            if default_value is not None:
                sql += f' DEFAULT {default_value}'

            # Execute the SQL statement to add the column
            self.cursor.execute(sql)

            # Check if 'additional_cols' exists in metadata, if not, initialize it
            if "additional_cols" not in self.metadata:
                self.metadata["additional_cols"] = []

            # Update metadata with the new column
            if column_name not in self.metadata["additional_cols"]:
                self.metadata["additional_cols"].append(column_name)
            self._save_metadata()

            # Commit the changes to the database
            self.conn.commit()
            print(f"Added column '{column_name}' to the records table with default value '{default_value}'.")

        except sqlite3.OperationalError as e:
            print(f"Error adding column '{column_name}': {e}")

    def update_column(self, key: str, column_name: str, value):
        try:
            # Update the specified column for the given key
            query = f'UPDATE {self.table_name} SET {column_name} = ? WHERE key = ?'
            self.cursor.execute(query, (value, key))
            if self.cursor.rowcount == 0:
                print(f"Record with key '{key}' does not exist.")
                return False
            self.conn.commit()
            print(f"Updated column '{column_name}' for key '{key}' with value '{value}'.")
            return True
        except sqlite3.OperationalError as e:
            print(f"Error updating column '{column_name}' for key '{key}': {e}")
            return False

    def close(self):
        self.conn.close()
