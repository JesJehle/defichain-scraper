import requests
import pandas
from datetime import date, datetime
from bs4 import BeautifulSoup
import os

# The main strategy is to use the market inefficiencies of the dex to make a constant profit.
# All stock tokes are constantly overpriced. This is due to the high demand and in constant changes. This changes can be used to buy when the price is low and sell when the prices are highter.
# The prices are the real dex prices of the stocks expressed as deviation of the oracle price. Since most stocks are overpriced the values range between 110 and 120 most of the time.
# For this to work, we need vary low volatile assets:
# dGLD - gold
# dSLV - silva
# dURTH - msci world etf
# For these assets I need the oracle prices and the dex prices


DEXPRICESURL = 'https://ocean.defichain.com/v0/mainnet/poolpairs'
ORACLEPRICESURL = 'https://ocean.defichain.com/v0/mainnet/prices'
RESULTS_PATH = "prices.csv"
stocks = [
    {
        "name": "GOLD",
        "dex_pair": "GLD-DUSD",
        "oracle_url": "https://defiscan.live/oracles/GLD-USD",
    },
    {
        "name": "SILVA",
        "dex_pair": "SLV-DUSD",
        "oracle_url": "https://defiscan.live/oracles/SLV-USD",
    },
    {
        "name": "MSCI",
        "dex_pair": "URTH-DUSD",
        "oracle_url": "https://defiscan.live/oracles/URTH-USD",
    },

]

dex_res = requests.get(DEXPRICESURL).json()


def parse_dex_price(stock_name):
    for stock in dex_res['data']:
        if stock['symbol'] == stock_name:
            return float(stock['priceRatio']['ba'])


def scrape_oracle_price(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = soup.find_all('h2', class_="text-4xl")
    return float(html[0].text.split(' ')[0])


df_dict = {}
df_dict['name'] = list()
df_dict['time'] = list()
df_dict['dex_price'] = list()
df_dict['oracle_price'] = list()
df_dict['dex_diff'] = list()

for stock in stocks:
    dex_price = parse_dex_price(stock['dex_pair'])
    oracle_price = scrape_oracle_price(stock['oracle_url'])
    df_dict['name'].append(stock['name'])
    df_dict['time'].append(datetime.now().strftime("%Y-%m-%d %H:%M"))
    df_dict['dex_price'].append(dex_price)
    df_dict['oracle_price'].append(oracle_price)
    df_dict['dex_diff'].append(dex_price * 100 / oracle_price)

df = pandas.DataFrame(df_dict)

if os.path.exists(RESULTS_PATH):
    df_old = pandas.read_csv(RESULTS_PATH)
    df = pandas.concat([df_old, df])
    df.to_csv('prices.csv', index=False)

else:
    df.to_csv('prices.csv', index=False)
