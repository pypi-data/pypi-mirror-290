class QueryBuilder:
    @staticmethod
    def get_last_timestamps(exchange: str) -> str:
        return f"""
        SELECT symbol, MAX(date) AS last_timestamp
        FROM {exchange}
        GROUP BY symbol;
        """

    @staticmethod
    def get_ohlcv(exchange: str, coin: str) -> str:
        return f"""
        SELECT date, open, high, low , close, volume
        FROM {exchange}
        WHERE symbol = '{coin}';
        """

    @staticmethod
    def get_ohlcv_time_bucket(exchange: str, coin: str, bucket: str = '15 minutes') -> str:
        return f"""
            SELECT
            time_bucket('{bucket}', date) AS period,
            first(open, date) AS open,
            max(high) AS high,
            min(low) AS low,
            last(close, date) AS close,
            sum(volume) AS volume
            FROM {exchange} WHERE symbol='{coin}' GROUP BY period
            ORDER BY period;
        """



    @staticmethod
    def csv_to_table(table: str) -> str:
        return f"""
                COPY {table} (date, open, high, low, close, volume, close_time, quote_asset_volume, n_trades, taker_buy_asset_volume, taker_buy_quote_asset_volume, symbol) FROM STDIN WITH CSV HEADER
                DELIMITER AS ','
        """

    @staticmethod
    def get_dataset(from_symbols: list, exchange: str) -> str:
        symbols = from_symbols
        base_query = """
        SELECT
            {coalesce_dates} AS date,
            {coalesce_columns}
        FROM
            (SELECT date, open, high, low, close FROM {exchange} WHERE symbol = '{symbol}') AS {alias}
        """

        joins = ""
        coalesce_dates = []
        coalesce_columns = []
        aliases = []

        for i, symbol in enumerate(symbols):
            alias = symbol.lower()
            aliases.append(alias)
            coalesce_dates.append(f"{alias}.date")
            coalesce_columns.extend([
                f"COALESCE({alias}.open, 0) AS {symbol}_open",
                f"COALESCE({alias}.high, 0) AS {symbol}_high",
                f"COALESCE({alias}.low, 0) AS {symbol}_low",
                f"COALESCE({alias}.close, 0) AS {symbol}_close"
            ])

            if i == 0:
                # The first symbol, no join needed
                continue

            # Generate join conditions for all previous aliases
            join_condition = " AND ".join(
                [f"COALESCE({prev_alias}.date, {alias}.date) = {alias}.date" for prev_alias in aliases[:-1]])
            joins += f"""
        FULL OUTER JOIN
            (SELECT date, open, high, low, close FROM {exchange} WHERE symbol = '{symbol}') AS {alias}
        ON {join_condition}
        """

        # Final SQL Query
        query = base_query.format(
            coalesce_dates="COALESCE(" + ", ".join(coalesce_dates) + ")",
            coalesce_columns=", ".join(coalesce_columns),
            symbol=symbols[0],
            alias=aliases[0],
            exchange=exchange
        ) + joins + " ORDER BY date ASC;"

        return query


