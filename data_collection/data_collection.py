from http_client import get_http_client, make_get_request
import config as conf

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os
import asyncio
import time
from tqdm import tqdm


load_dotenv()

async def get_intervals(start_date:str=None, end_date:str=None, bin_size:int=10) -> list[tuple[str]]:
    '''
    Creates list of dateranges of bin_size days
    '''
    period_years, year_size = 10, 365
    
    if end_date is None:
        end_date = datetime.now()
        start_date = end_date-timedelta(days=period_years * year_size)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    datarange = pd.date_range(start=start_date, end=end_date)
    intervals = [(datarange[i].strftime("%Y-%m-%d"), datarange[i+bin_size-1].strftime("%Y-%m-%d")) for i in range(0, len(datarange)-bin_size+1, bin_size)]
    return intervals


async def get_tickers()->list[str]:
    '''
    Gets table with Stocks Tickers from Wikipedia
    '''
    sp_500_wiki_info = pd.read_html(conf.wiki_tickers_url, attrs={'id':'constituents'})[0]
    sp_500_tickers = sp_500_wiki_info['Symbol'].to_list() + ['SPY']
    return sp_500_tickers


async def urls_constructor(ticker, start_date, end_date, timespan, multiplier)->list[str]:
    '''
    Constructs list of urls for Polygon API endpoints
    '''
    token = os.environ['PTOKEN']
    intervals = await get_intervals(start_date, end_date, 20)
    urls = []
    for _ in intervals:
        urls.append(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{_[0]}/{_[1]}?adjusted=true&sort=asc&limit=5000&apiKey={token}')
    return urls


async def get_data(ticker, start_date, end_date, timespan, multiplier)->pd.DataFrame:
    '''
    Asynchronously makes requests to Polygon API.
    Joins results into a single DataFrame
    '''
    urls = await urls_constructor(ticker, start_date, end_date, timespan, multiplier)
    async with get_http_client(conf.headers) as http_client:
        tasks = [make_get_request(http_client, url, conf.headers) for url in urls]
        results = await asyncio.gather(*tasks)

    frames, additional_urls = [], []
    for r in results:
        if r is None:
            continue
        frames.append(pd.DataFrame(r['results']))
        if 'next_url' in r:
            additional_urls.append(r['next_url'])

    # additional walk
    async with get_http_client(conf.headers) as http_client:
        tasks = [make_get_request(http_client, url, conf.headers) for url in additional_urls]
        results = await asyncio.gather(*tasks)

    for r in results:
        if r is None:
            continue
        frames.append(pd.DataFrame(r['results']))

    return pd.concat(frames, ignore_index=True)


async def main():

    # now, end_date = datetime.now(), datetime.now().strftime("%Y-%m-%d")
    # start_date = (now-timedelta(days= 10 * 365)).strftime("%Y-%m-%d")

    start_date = '2020-01-01'
    end_date = datetime.now().strftime("%Y-%m-%d")

    tickers = await get_tickers()
    exceptions = []

    for ticker in tqdm(tickers[:3]):
        # try:
        data = await get_data(ticker, start_date, end_date, conf.timespan, conf.multiplier)
        result_file_name = f'./{conf.data_dir}/{ticker}_{conf.multiplier}_{conf.timespan}_stock_prices_1.csv'
        data.to_csv(result_file_name, index=False)
        time.sleep(30)

        # except:
        #     exceptions.append(ticker)
        #     log_frame = pd.DataFrame(data={'ticker': exceptions})
        #     log_frame.to_csv(f'./{conf.data_dir}/exceptions.csv', index=False)
        #     time.sleep(30)
        #     continue
    
asyncio.run(main()) 