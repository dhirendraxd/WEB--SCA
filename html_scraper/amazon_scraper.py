from datetime import datetime
import requests
import csv
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

def get_page_html(url):
    try:
        res = requests.get(url=url, headers=REQUEST_HEADER)
        res.raise_for_status()  # Check if the request was successful
        return res.content
    except requests.RequestException as e:
        print(f'Error fetching the page HTML: {e}')
        return None

def get_product_price(soup):
    try:
        main_price_span = soup.find('span', attrs={'class': 'a-price-whole'})
        if not main_price_span:
            return None
        price = main_price_span.text.strip().replace('$', '').replace(',', '')
        return price
    except AttributeError:
        return None

def get_product_title(soup):
    try:
        product_title = soup.find('span', id='productTitle')
        if not product_title:
            return None
        return product_title.text.strip()
    except AttributeError:
        return None

def extract_product_info(url):
    product_info = {}
    print(f'Scraping URL: {url}')
    html = get_page_html(url=url)
    if html is None:
        product_info['error'] = 'Failed to retrieve the page'
        return product_info

    soup = BeautifulSoup(html, "lxml")
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)

    return product_info

if __name__ == "__main__":
    with open('amazon_Products_urls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            product_info = extract_product_info(url)
            print(product_info)