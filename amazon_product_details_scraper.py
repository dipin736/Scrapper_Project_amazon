import csv
import requests
from bs4 import BeautifulSoup
from time import sleep
from amazon_scraper import scrape_product_listing


def scrape_product_details(product_data):
    for product in product_data:
        url = product['Product URL']
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch product details for URL: {url}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        asin_element = soup.find('th', text='ASIN')
        asin = asin_element.find_next('td').text.strip() if asin_element else 'N/A'

        description = soup.find('meta', {'name': 'description'})['content'].strip()

        manufacturer_element = soup.find('a', {'id': 'bylineInfo'})
        manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

        product['ASIN'] = asin
        product['Description'] = description
        product['Manufacturer'] = manufacturer

        sleep(2)

if __name__ == "__main__":
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    num_pages = 20

    product_data = scrape_product_listing(base_url, num_pages)

    scrape_product_details(product_data)

    csv_filename = 'amazon_products.csv'

    with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'ASIN', 'Description', 'Manufacturer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)

    print(f"Data has been scraped and exported to {csv_filename}.")
