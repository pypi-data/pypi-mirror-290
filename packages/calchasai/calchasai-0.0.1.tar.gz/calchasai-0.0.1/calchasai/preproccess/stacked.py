import pandas as pd

class StackedCsv:
    """
    StackedFile is a class that concatenates vertically
    all the same csv files of all the datasets with chronological order
    based on the priority that the class is instantiated with. For example
    given as priority attribute the list ['Binance','Bitstamp','Kraken'],
    the resulting stacked dataframe will have first the rows and cols of Kraken,
    then Bitstamp's and then Binance's  a more visual example bellow


            --- Kraken   ---
            --- Bitstamp ---
            --- Binance  ---


    Attributes:
        file_name (str): The name for the coin to stack
        priority (list): A list that has the exchange names with the desired order for the vertical stack.

    """
    def __init__(self,coin_name:str,priority:list):
        self.coin_name = coin_name
        self.priority = priority


    @staticmethod
    def combine_dfs(priority_df: pd.DataFrame, supplementary_df: pd.DataFrame) -> pd.DataFrame:
        priority_df['date'] = pd.to_datetime(priority_df['date'])
        supplementary_df['date'] = pd.to_datetime(supplementary_df['date'])

        # Find the first date in the smaller DataFrame
        first_date_priority = priority_df['date'].min()
        # Filter the larger DataFrame to keep rows up to the first date of the smaller DataFrame
        supplementary_filtered = supplementary_df[supplementary_df['date'] < first_date_priority]

        # Concatenate the filtered larger DataFrame with the smaller DataFrame
        result_df = pd.concat([supplementary_filtered, priority_df])
        result_df = result_df.sort_values(by='date').reset_index(drop=True)
        return result_df






