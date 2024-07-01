import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import concurrent.futures 
from tqdm import tqdm

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}
NO_THREADS = 10

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

def get_product_rating(soup):
    try:
        product_rating_section = soup.find('span', attrs={'class': 'a-icon-alt'})
        if not product_rating_section:
            return None
        rating_text = product_rating_section.text.strip().split(" ")[0]
        return float(rating_text)
    except (AttributeError, ValueError):
        return None

def get_product_technical_details(soup):
    details = {}
    try:
        technical_details_section = soup.find('div', id="detailBullets_feature_div")
        if not technical_details_section:
            return details
        
        for bullet in technical_details_section.find_all('li'):
            spans = bullet.find_all('span')
            if len(spans) == 2:
                key = spans[0].text.strip().replace(':', '')
                value = spans[1].text.strip()
                details[key] = value
    except AttributeError as e:
        print(f"Error extracting technical details: {e}")
    return details

def extract_product_info(url):
    product_info = {}
    html = get_page_html(url)
    if html is None:
        product_info['error'] = 'Failed to retrieve the page'
        return product_info

    soup = BeautifulSoup(html, "html.parser")
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['rating'] = get_product_rating(soup)
    product_info.update(get_product_technical_details(soup))

    return product_info

if __name__ == "__main__":
    product_data = []
    urls = []
    with open('amazon_Products_urls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append(row[0])  # assuming the URL is in the first column

    with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
        results = list(tqdm(executor.map(extract_product_info, urls), total=len(urls)))

    output_file_name = f'output-{datetime.today().strftime("%m-%d-%y")}.csv'
    with open(output_file_name, 'w', newline='') as outputfile:
        writer = csv.DictWriter(outputfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Scraping complete. Data saved to {output_file_name}")
