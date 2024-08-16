import psycopg2
import pytest

db_host = 'localhost'
db_database = 'postgres'
db_user = 'postgres'
db_password = 'password'


def is_database_available():
    try:
        # Try to create a connection (adjust with your connection details)
        conn = psycopg2.connect(dbname=db_database,user=db_user,password=db_password,host=db_host)
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False



@pytest.mark.skipif(not is_database_available(), reason="Database not available!")
def test_conn():


    conn = psycopg2.connect(dbname=db_database,user=db_user,password=db_password,host=db_host)
    cursor = conn.cursor()
    query = f"""
                SELECT
                time_bucket('15 minutes', date) AS period,
                first(open, date) AS open,
                max(high) AS high,
                min(low) AS low,
                last(close, date) AS close,
                sum(volume) AS volume
                FROM Binance WHERE symbol='XRPUSDT' GROUP BY period
                ORDER BY period;
            """
    cursor.execute(query)
    res = cursor.fetchall()
    assert len(res)>1

