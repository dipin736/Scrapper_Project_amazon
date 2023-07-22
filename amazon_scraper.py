import csv
import requests
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urljoin


def scrape_product_listing(url, pages=20):
    data = []

    for page_num in range(1, pages + 1):
        page_url = url + f'&page={page_num}'
        response = requests.get(page_url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page_num}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})

        for card in product_cards:
            product_url_relative = card.find('a', {'class': 'a-link-normal'})['href']
            product_url = urljoin('https://www.amazon.in/', product_url_relative)  # Convert to absolute URL

            product_name = card.find('span', {'class': 'a-size-medium'}).text.strip()
            product_price = card.find('span', {'class': 'a-offscreen'}).text.strip()

            rating_element = card.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.text.split()[0] if rating_element else 'N/A'

            num_reviews_element = card.find('span', {'class': 'a-size-base'})
            num_reviews = num_reviews_element.text if num_reviews_element else '0'

            data.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of Reviews': num_reviews
            })

        sleep(2)

    return data



if __name__ == "__main__":
        base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
        num_pages = 20

        product_data = scrape_product_listing(base_url, num_pages)


        csv_filename = 'amazon_products.csv'

        with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(product_data)

        print(f"Data has been scraped and exported to {csv_filename}.")

