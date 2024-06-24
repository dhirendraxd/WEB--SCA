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
    print(f'Scraping URL: {url}')
    html = get_page_html(url=url)
    if html is None:
        product_info['error'] = 'Failed to retrieve the page'
        return product_info

    soup = BeautifulSoup(html, "lxml")
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['rating'] = get_product_rating(soup)
    product_info.update(get_product_technical_details(soup))

    # Debugging information
    print(f"Product Title: {product_info.get('title')}")
    print(f"Product Price: {product_info.get('price')}")
    print(f"Product Rating: {product_info.get('rating')}")
    print(f"Technical Details: {product_info}")

    return product_info

if __name__ == "__main__":
    with open('amazon_Products_urls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        with open('amazon_products_info.csv', mode='w', newline='') as outfile:
            # Determine all possible fields dynamically
            fieldnames = set()
            product_infos = []

            for row in reader:
                url = row[0]
                product_info = extract_product_info(url)
                product_infos.append(product_info)
                fieldnames.update(product_info.keys())

            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for product_info in product_infos:
                writer.writerow(product_info)
