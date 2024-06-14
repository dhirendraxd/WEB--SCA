from datetime import datetime
import requests
import csv
import bs4


USER_AGENT ="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

REQUEST_HEADER = {
    'User-Agent' : USER_AGENT,
    'Accept-Language':'en-US, en;q=0.5',
    
}

def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def extract_product_info(url):
    product_info = {}
    print(f'Scraping URL:{url}')
    html =get_page_html(url=url) 
    print(html)

if __name__ == "__main__":
    with open('amazon_Products_urls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')  
        for row in reader:
            url = row[0]
            print(extract_product_info(url))

