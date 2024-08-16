import re
from functools import reduce
import pandas as pd
import os
from .utils import get_paths


class CsvReader:
    DATASET_DIR_PATH = 'datasets'
    def __init__(self, freq: str, dataset: str, columns_to_drop: list[str] | str | None = None):
        self.columns_to_drop = columns_to_drop
        self.freq = freq
        self.dataset = dataset
        self._dfs = None
        self._merged = None
        self._read_dfs()
        self._merge_dfs()

    def _merge_dfs(self):
        self._merged = reduce(lambda left, right: pd.merge(left, right, on='date', how='outer'), self._dfs)
        self._merged.index = self._merged.date
        self._merged.sort_index(ascending=True, inplace=True)

    def _read_dfs(self):
        dfs = []
        paths = get_paths(freq=self.freq, dataset=self.dataset)
        for path in paths:
            coin = path.split('_')[0]
            df = pd.read_csv(os.path.join(self.DATASET_DIR_PATH, self.dataset, path))
            if self.columns_to_drop:
                self._drop_columns(df)
            columns = df.columns
            new_columns = [f'{coin}_' + col for col in df.columns if col != 'date']
            new_columns.insert(0, 'date')
            df.columns = new_columns
            dfs.append(df)

        self._dfs = dfs

    def _drop_columns(self, df: pd.DataFrame) -> None:
        df.drop(self.columns_to_drop, axis=1, inplace=True)

    @property
    def df(self):
        return self._merged


