import os
from typing import Optional
import psycopg2
import pandas as pd
import re

from calchasai.data_service.queries import QueryBuilder

db_host = 'localhost'
db_database = 'postgres'
db_user = 'postgres'
db_password = 'password'


class Db:
    def __init__(self):
        self.cursor: Optional[psycopg2.cursor] = None
        self.conn: Optional[psycopg2.connection] = None

        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(user=db_user, password=db_password, host=db_host, port=5432)
            print("connected to db")
        except psycopg2.OperationalError as e:
            print("Unable to connect to the database. Check your connection settings.")
            print(e)

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()



    def create_binance_table(self):
        cursor = self.conn.cursor()

        create_hypertable_query = """
            CREATE TABLE Binance (
                date TIMESTAMPTZ  NOT NULL,
                open DOUBLE PRECISION NOT NULL,
                high DOUBLE PRECISION NOT NULL,
                low DOUBLE PRECISION NOT NULL,
                close DOUBLE PRECISION NOT NULL,
                volume DOUBLE PRECISION NOT NULL,
                close_time TIMESTAMPTZ, 
                quote_asset_volume DOUBLE PRECISION NOT NULL,
                n_trades INTEGER NOT NULL,
                taker_buy_asset_volume DOUBLE PRECISION NOT NULL,
                taker_buy_quote_asset_volume DOUBLE PRECISION NOT NULL,
                symbol TEXT NOT NULL
            );
            SELECT create_hypertable('Binance', 'date');
        """

        cursor.execute(create_hypertable_query)
        self.conn.commit()
        cursor.close()

    def insert_csv_to_table(self, csv_file_path, table_name):

        try:
            with open(csv_file_path, 'r') as f:
                symbol = csv_file_path.split('_')[0]
                cursor = self.conn.cursor()
                try:

                    copy_sql = f"""
                    COPY {table_name} (date, open, high, low, close, volume, close_time, quote_asset_volume, n_trades, taker_buy_asset_volume, taker_buy_quote_asset_volume, symbol) FROM STDIN WITH CSV HEADER
                    DELIMITER AS ','
                    """

                    cursor.copy_expert(sql=copy_sql, file=f)
                    self.conn.commit()
                    rows_inserted = cursor.rowcount
                    print(f"Coin:{symbol}, Number of rows inserted: {rows_inserted}")
                except psycopg2.errors.UniqueViolation as e:
                    print(f"Duplicate key error for {csv_file_path}: {e}")
                    self.conn.rollback()
                except Exception as e:
                    print(f"Error loading CSV to table {csv_file_path}: {e}")
                    self.conn.rollback()
                finally:
                    cursor.close()


        except Exception as e:
            print("Error loading CSV to table: ", e)

    def insert_all_to_table(self, csv_folder_path: str, table_name: str, freq: str) -> None:

        for csv_file_path in os.listdir(csv_folder_path):
            if freq in csv_file_path:
                csv_file_path = os.path.join(csv_folder_path, csv_file_path)
                self.insert_csv_to_table(csv_file_path, table_name)

    def add_unique_constraint(self):
        try:
            # Connect to your PostgreSQL database

            # Create a cursor object
            cursor = self.conn.cursor()

            # Define the SQL command to add the unique constraint
            alter_table_query = """
            ALTER TABLE binance 
            ADD CONSTRAINT unique_timestamp_symbol 
            UNIQUE (date, symbol);
            """

            # Execute the SQL command
            cursor.execute(alter_table_query)

            # Commit the transaction
            self.conn.commit()

            print("Unique constraint added successfully.")

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()

    def get_last_timestamp(self, exchange='binance') -> pd.DataFrame:
        query = QueryBuilder.get_last_timestamps(exchange)
        cursor = self.conn.cursor()
        cursor.execute(query=query)
        data = cursor.fetchall()
        cursor.close()

        df = pd.DataFrame(data, columns=['symbol', 'date'])
        df = df.set_index('symbol').T

        return df


