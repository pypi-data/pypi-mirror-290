import time
import pandas as pd
from datetime import datetime
from calchasai.downloader.base_downloader import BaseDownloader
from calchasai._coins import BitstampCoins as Coins
from pytz import utc
import os
from calchasai.preproccess.utils import get_paths
class BitstampDownloader(BaseDownloader):
    BASE_URL = 'https://www.bitstamp.net/api/v2/'
    OHLC_ENDPOINT = 'https://www.bitstamp.net/api/v2/ohlc/'
    PAIRS_ENDPOINT = 'https://www.bitstamp.net/api/v2/trading-pairs-info/'
    CSV_SAVE_PATH = os.path.join('datasets','Bitstamp')
    PATH = os.path.join('datasets', 'Bitstamp')
    PATH_UPDATES = os.path.join(PATH, 'db')
    def __init__(self):
        super().__init__()
        self._failed_downloading = []
        self._freq = None
        self.ohlc_list = None
        self.params = {
            'limit': 800,
            'step': 60
        }
        self.df_types = {'close': float, 'high': float, 'low': float, 'open': float, 'volume': float, 'timestamp': int}
        self._coin_name = None
        self._make_dirs()
    @property
    def df(self) -> pd.DataFrame:
        if not self._freq:
            raise RuntimeError("The 'get_ohlc' method must be executed before accessing 'df'")
        else:

            df = pd.DataFrame(self.ohlc_list)
            df = df.astype(self.df_types)

            df.rename(columns={'timestamp': 'date', 'open': 'Open', 'high': 'High',
                               'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
            df = df[['date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df.date = df.date.apply(lambda x: datetime.fromtimestamp(x, tz=utc))

            # fill missing dates

            duplicate_mask = df.duplicated('date', keep='first')
            duplicated_dates = df[duplicate_mask]

            if not duplicated_dates.empty:
                df = df[~duplicate_mask]

            df = self._fill_missing_dates(df, self._freq)

            return df

    def get_pairs(self):
        pass

    def _make_dirs(self) -> None:
        if 'datasets' not in os.listdir():
            os.mkdir('datasets')
            os.mkdir(self.PATH)
        if 'Bitstamp' not in os.listdir('datasets'):
            os.mkdir(self.PATH)
        if not os.path.exists(self.PATH_UPDATES):
            os.mkdir(self.PATH_UPDATES)

    def get_ohlc(self, coin: str = None, start: str = None, end: str = None, freq: str = '1h') -> pd.DataFrame:
        self._coin_name = coin
        valid_frequencies = {'1m', '5m', '15m', '1h','1d'}
        freq_map = {'1m': 60, '3m': 180, '5m': 300, '15m': 900, '1h': 3600,'1d':3600*24}
        if freq not in valid_frequencies:
            raise ValueError(f"Invalid freqeuency {freq}. Must be one of [1m, 3m, 5m, 15m, 1h]")

        if start is not None:
            start_timestamp = self._date_to_timestamp(start)
            self.params.update({'start': start_timestamp})
        if end is not None:

            end_timestamp = self._date_to_timestamp(end)
            self.params.update({'end_timestamp': end_timestamp})

        else:
            now = datetime.now()
            rounded = datetime(now.year, now.month, now.day, now.hour)
            self.params['end_timestamp'] = int(rounded.timestamp())

        self.params.update({'step': freq_map[freq]})

        # response_json = self._get(self.OHLC_ENDPOINT + f'{coin}/', params=self.params)
        # ohlc_list = response_json['data']['ohlc']
        # last_timestamp = ohlc_list[-1]['timestamp']
        # self.params['start'] = last_timestamp

        # df = pd.DataFrame(response_json['data']['ohlc'])

        ohlc_list = self._get_all_ohlc(coin)
        self.ohlc_list = ohlc_list
        self._freq = freq

        return ohlc_list

    def _get_single_ohlc(self, coin: str = None, save: bool = False):
        response_json = self._get(self.OHLC_ENDPOINT + f'{coin}/', params=self.params)
        ohlc_list = response_json['data']['ohlc']
        if ohlc_list:
            last_timestamp = int(ohlc_list[-1]['timestamp']) + self.params['step']
        else:
            last_timestamp = self.params['start'] + 86400
            print('searching for fist date')
        self.params['start'] = int(last_timestamp)
        return ohlc_list

    def _get_all_ohlc(self, coin: str):
        ohlc_list = self._get_single_ohlc(coin)
        while self.params['start'] < self.params['end_timestamp']:
            if self.request_counter < 7800:
                ohlc_list += self._get_single_ohlc(coin)
            else:
                time.sleep(15 * 60)
                self._reset_request_counter()

        return ohlc_list

    def _fill_missing_dates(self, df: pd.DataFrame, freq: str):
        freq_map = {'1m': '1min','5m':'5min','15m': '15min', '1h': '1h','1d':'1d'}

        df.index = pd.to_datetime(df.date)
        resampled_df = df.resample(freq_map[self._freq]).bfill()
        resampled_df.date = resampled_df.index
        return resampled_df

    def download_all(self, freq: str = '1h', from_date: str = '2020-03-20', export: bool = False) -> None:
        downloads = self._get_downloads(freq=freq)
        for coin in Coins:
            if coin.value not in downloads:
                print(f"downloading {coin.value}")
                self.get_ohlc(coin=coin.value,start=from_date,freq=freq)
                if not self.df.empty:

                    if export:
                        self.export_df()
                else:
                    print(f"\033[91mWARNING: DataFrame {coin.value} is empty. No data to process.\033[0m")
                    self._failed_downloading.append(coin.value)

    def export_df(self,path = CSV_SAVE_PATH):
        if not os.path.exists(path):
            os.makedirs(path)

        file_name = self._coin_name +'_' + self._freq + '.csv'
        self.df.to_csv(os.path.join(path,file_name),index=False)


    def _get_downloads(self, freq):
        downloads = get_paths(freq, 'Bitstamp')
        downloads = [d.split('_')[0] for d in downloads]
        return downloads

