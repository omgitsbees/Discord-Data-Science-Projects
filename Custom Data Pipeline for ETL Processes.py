import pandas as pd
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data(file_path):
    """Extract data from CSV file."""
    logging.info("Starting data extraction...")
    try:
        data = pd.read_csv(file_path)
        logging.info("Data extraction completed successfully.")
        return data
    except Exception as e:
        logging.error(f"Error during data extraction: {e}")
        return None

def transform_data(data):
    """Transform the data."""
    logging.info("Starting data transformation...")
    try:
        # Example transformations: remove duplicates and fill missing values
        data = data.drop_duplicates()
        data.fillna(method='ffill', inplace=True)
        logging.info("Data transformation completed successfully.")
        return data
    except Exception as e:
        logging.error(f"Error during data transformation: {e}")
        return None

def load_data(data, db_name, table_name):
    """Load data into SQLite database."""
    logging.info("Starting data loading...")
    try:
        conn = sqlite3.connect(db_name)
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        logging.info("Data loading completed successfully.")
    except Exception as e:
        logging.error(f"Error during data loading: {e}")

def main(file_path, db_name, table_name):
    """Main function to run the ETL pipeline."""
    data = extract_data(file_path)
    if data is not None:
        transformed_data = transform_data(data)
        if transformed_data is not None:
            load_data(transformed_data, db_name, table_name)

if __name__ == "__main__":
    # Define file path and database parameters
    CSV_FILE_PATH = 'data.csv'  # Path to your CSV file
    DATABASE_NAME = 'etl_database.db'
    TABLE_NAME = 'transformed_data'

    main(CSV_FILE_PATH, DATABASE_NAME, TABLE_NAME)
