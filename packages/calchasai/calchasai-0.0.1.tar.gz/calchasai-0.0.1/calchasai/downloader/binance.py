import pandas as pd
from datetime import datetime
from binance.client import Client
import os
from calchasai._coins import BinanceCoins as Coins
from pytz import utc
from calchasai.data_service.db import Db
import io
from .utils import get_timedelta_for_freq




class BinanceDownloader:
    ALLOWED_FREQUENCIES = ['1m', '3m', '5m', '15m', '1h', '1d']
    PATH = os.path.join('datasets', 'Binance')
    PATH_UPDATES = os.path.join(PATH, 'db')
    BINANCE_PANDAS_MAPPING = {"5m": "5min", "1m": "1min", "15m": "15min", "1h": "1h", "1d": "D", "d": "D"}

    def __init__(self, use_database: bool = False) -> None:
        self.client = Client()
        self._make_dirs()
        self._failed_downloading: list = []
        self.use_database: bool = False
        if use_database:
            self.db = Db()
            self.use_database = True

    def _clean_data(self, df: pd.DataFrame, freq: str) -> pd.DataFrame:

        # drop duplicates
        df = df[~df.date.duplicated(keep='first')]
        # create the full date range
        full = pd.date_range(start=df['date'].iloc[0], end=df['date'].iloc[-1],
                             freq=self.BINANCE_PANDAS_MAPPING[freq])
        df.index = df.date
        # fill missing timesteps
        df = df.resample(self.BINANCE_PANDAS_MAPPING[freq]).asfreq().bfill()
        # set the date column to be the full date range
        df.date = df.index
        return df

    def _cast_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Casts columns to the appropriate data types."""
        try:
            # Cast the columns to their appropriate types
            df['Open'] = df['Open'].astype('float64')
            df['High'] = df['High'].astype('float64')
            df['Low'] = df['Low'].astype('float64')
            df['Close'] = df['Close'].astype('float64')
            df['Volume'] = df['Volume'].astype('float64')
            df['Close time'] = pd.to_datetime(df['Close time'], utc=True)
            df['Quote asset Volume'] = df['Quote asset Volume'].astype('float64')
            df['n_trades'] = df['n_trades'].astype('int64')
            df['taker buy asset volume'] = df['taker buy asset volume'].astype('float64')
            df['taker buy quote asset volume'] = df['taker buy quote asset volume'].astype('float64')
            return df
        except KeyError as e:
            print(f"Error casting columns: Missing column {e}")
        except Exception as e:
            print(f"Error casting columns: {e}")

    def _freq_allowed(self, freq: str) -> bool:
        if freq not in self.ALLOWED_FREQUENCIES:
            return False
        else:
            return True

    def _export_dataset(self, df: pd.DataFrame, coin: str, freq: str) -> None:
        self._make_dirs()
        df.to_csv(os.path.join(self.PATH, f'{coin}_{freq}.csv'), index=False)

    def _download_single(self, coin: str, freq: str, from_date: str) -> pd.DataFrame:
        if not self._freq_allowed(freq):
            raise ValueError(f"Frequency '{freq}' is not allowed. Allowed frequencies are: {self.ALLOWED_FREQUENCIES}")

        klines = self.client.get_historical_klines(coin, freq, from_date)
        col_names = ["date", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset Volume",
                     "n_trades",
                     "taker buy asset volume", "taker buy quote asset volume", "ignore"]
        df = pd.DataFrame(klines, columns=col_names)
        df["date"] = (df["date"] / 1000).apply(lambda x: datetime.fromtimestamp(x, tz=utc))
        df["Close time"] = (df["Close time"] / 1000).apply(lambda x: datetime.fromtimestamp(x, tz=utc))
        df.drop(columns='ignore', inplace=True)
        if self.use_database:
            df['symbol'] = coin
        return df

    def _export_dataset_db(self, df: pd.DataFrame, coin: str, freq: str) -> None:
        self._make_dirs()
        df.to_csv(os.path.join(self.PATH_UPDATES, f'{coin}_{freq}.csv'), index=False)

    def _make_dirs(self) -> None:
        if 'datasets' not in os.listdir():
            os.mkdir('datasets')
            os.mkdir(self.PATH)
        if 'Binance' not in os.listdir('datasets'):
            os.mkdir(self.PATH)
        if not os.path.exists(self.PATH_UPDATES):
            os.mkdir(self.PATH_UPDATES)

    def download_all(self, freq: str = '1h', from_date: str = '2 days ago', export: bool = False,
                     insert_to_db: bool = False) -> None:

        for coin in Coins:
            print(f"downloading {coin.value}")
            df = self._download_single(coin.value, freq, from_date)
            if not df.empty:

                df = self._clean_data(df, freq)
                df = self._cast_columns(df)

                if export:
                    self._export_dataset(df, coin.value, freq)

                if self.use_database and insert_to_db:
                    self.insert_to_db(table_name='binance')

            else:
                print(f"\033[91mWARNING: DataFrame {coin.value} is empty. No data to process.\033[0m")
                self._failed_downloading.append(coin.value)

    def update_all(self, freq: str = '1h', export: bool = False, insert_to_db: bool = False) -> None:
        """
        Update the database with new data for each coin starting from the last recorded timestamp plus the frequency.

        Args:
            freq (str): Frequency of the data to download. Default is '1h'.
            export (bool): Whether to export the updated data to CSV. Default is False.
            insert_to_db (bool): Whether to insert the updated data into the database. Default is False.
        """

        timestamp_df = self.db.get_last_timestamp('binance')
        print("last timestamps for each coin: \n", timestamp_df)

        for coin in timestamp_df:
            from_date = str(timestamp_df[coin].iloc[0] + get_timedelta_for_freq(freq))
            df = self._download_single(coin=coin, freq=freq, from_date=from_date)
            print(df)
            if len(df) > 1:
                df = self._clean_data(df=df, freq=freq)
            if export:
                self._export_dataset_db(df=df, coin=coin, freq=freq)
            if self.use_database and insert_to_db:
                self.insert_to_db(df=df, table_name='binance')

    def insert_to_db(self, df: pd.DataFrame, table_name: str) -> None:
        """Insert the current DataFrame (_df) into the specified database table."""

        if df.empty:
            print("No data available to insert into the database.")
            return
        try:
            # Establish a connection to your database

            conn = self.db.conn
            cursor = conn.cursor()

            # Convert DataFrame to CSV format in memory
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            # Define the COPY SQL statement
            copy_sql = f"""
               COPY {table_name} (date, open, high, low, close, volume, close_time, quote_asset_volume, n_trades, taker_buy_asset_volume, taker_buy_quote_asset_volume, symbol)
               FROM STDIN WITH CSV HEADER
               DELIMITER AS ','
               """
            cursor.copy_expert(copy_sql, csv_buffer)
            conn.commit()

            print(f"Data successfully inserted into {table_name}")

        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")
            conn.rollback()
        finally:
            cursor.close()
