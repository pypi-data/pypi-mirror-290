# CryptoDataDownloader


## Quick Start

**Minimal Example**

```python


from calchasai.downloader import BinanceDownloader
from calchasai.preproccess import CsvReader


loader = BinanceDownloader()
loader.download_all('15m', from_date='3 days ago', export=True)

reader = CsvReader('15m', 'Binance')

df = reader.df

```


**Run the db_sync.py deamon inside docker**

```
docker build -t db-sync-deamon .    
docker run -d  --name db-sync-deamon --network db_calchasdb  db-sync-deamon
```
