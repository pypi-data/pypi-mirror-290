import polars as pl
import os



def add_symbol_col(path:str):
    for file_path in os.listdir(path):
        symbol_name = file_path.split("_")[0]
        df = pl.read_csv(os.path.join(path,file_path))
        df = df.with_columns([pl.lit(symbol_name).alias("symbol")])
        df.write_csv(os.path.join(path,file_path))


def add_symbol_col(path: str):
    # Iterate over all files in the directory
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        # Check if it's a file and if it ends with .csv
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            symbol_name = file_name.split("_")[0]
            df = pl.read_csv(file_path)

            # Add the 'symbol' column with the extracted symbol name
            df = df.with_columns([pl.lit(symbol_name).alias("symbol")])

            # Write the updated DataFrame back to the same CSV file
            df.write_csv(file_path)
        else:
            print(f"Skipping {file_name}: not a valid CSV file.")


def cast_col_to(col,type):
    """
    Function that casts a polars dataframe column to a
    specific data type

    :param col:
    :param type:
    :return:
    """
    pass