import redis
import requests
from bs4 import BeautifulSoup
import json

def scrape_data():
    url = 'https://www.nseindia.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example scraping logic for the 'Nifty 50' table
    nifty_data = []
    # Note: Update the scraping logic based on the actual HTML structure of the table.
    table = soup.find('table', {'id': 'nifty_table'})
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            nifty_data.append([ele for ele in cols if ele])  # Get rid of empty values

    # Store data in Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    nifty_data_json = json.dumps(nifty_data)
    r.set('nifty_data', nifty_data_json)
