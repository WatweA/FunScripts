#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import json
import pandas as pd


def print_random():
    ishares_url = 'https://www.ishares.com'
    russel1000_url = ishares_url + '/us/products/239707/ishares-russell-1000-etf#'

    # scrape the iShares Russell 1000 ETF webpage
    ishares_website_request = urllib.request.Request(url=russel1000_url)
    ishares_website_string = urllib.request.urlopen(ishares_website_request).read().decode('UTF-8')
    ishares_website_soup = BeautifulSoup(ishares_website_string, 'html.parser')

    # retrieve the table headers from the components list table
    holdings_table = ishares_website_soup.find(id="allHoldingsTab", recursive=True)
    headers = [value.text.strip() for value in holdings_table.find_all('th')]

    # retrieve the table data json
    json_ajax_target = ishares_url + holdings_table.get('data-ajaxuri')
    components_json_reqest = urllib.request.Request(url=json_ajax_target)
    components_json_string = urllib.request.urlopen(components_json_reqest).read().decode('utf-8-sig')
    components_json_data = json.loads(components_json_string)
    components_df = pd.DataFrame(components_json_data['aaData'], columns=headers)

    # extract numerical data from dictionaries - default to 0
    def get_raw_float(data_dict): return float(data_dict.get('raw', 0.0))

    components_df.loc[:, ['Market Value', 'Weight (%)', 'Notional Value', 'Price']] = \
        components_df.loc[:, ['Market Value', 'Weight (%)', 'Notional Value', 'Price']].applymap(get_raw_float)

    def get_raw_int(data_dict): return int(data_dict.get('raw', 0))

    components_df.loc[:, ['Shares']] = components_df.loc[:, ['Shares']].applymap(get_raw_int)

    print("a random selection of 10 stocks from the iShares Russell 1000 ETF:")
    print(components_df.sample(n=10))


if __name__ == '__main__':
    print_random()
