import os
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
from urllib.parse import urlparse
import imghdr
import base64
from io import BytesIO
from PIL import Image

class MyWebScraper:
    def __init__(self, url):
        self.url = url

    def _make_request(self, url, headers=None):
        try:
            if url.startswith('data:'):
                # Handle data URL
                img_data = url.split(',')[1]
                img_bytes = base64.b64decode(img_data)
                response = BytesIO(img_bytes)
                response.content = img_bytes
            else:
                # Handle regular HTTP/HTTPS URL
                if headers is None:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

            return response

        except requests.RequestException as e:
            logging.error(f"Error during request: {e}")
            return None

    def get_quotes(self, elements=['div', 'p', 'blockquote', 'span', 'q']):
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            quotes = []
            for element in elements:
                for quote_elem in soup.find_all(element):
                    quote = quote_elem.get_text().strip()
                    quotes.append(quote)

            return quotes

        except requests.RequestException as e:
            logging.error(f"Error during request: {e}")
            return []

    def save_quotes_to_file(self, quotes, filename='quotes.txt'):
        try:
            output_path = os.path.join(os.getcwd(), filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                for quote in quotes:
                    file.write(f"{quote}\n")
            logging.info(f"Quotes saved to {output_path}")

        except Exception as e:
            logging.error(f"Error while saving quotes to file: {e}")

    def scrape_images(self, save_folder='images'):
        try:
            os.makedirs(save_folder, exist_ok=True)
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = self._make_request(self.url, headers=headers)
            if not response:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            image_urls = []
            for img_elem in soup.find_all('img', src=True):
                img_url = urljoin(self.url, img_elem['src'])
                image_urls.append(img_url)

                # Generate a valid filename from the URL
                img_filename = os.path.basename(urlparse(img_url).path)
                img_filepath = os.path.join(save_folder, img_filename)

                # Download and save the image
                img_response = self._make_request(img_url, headers=headers)
                if img_response:
                    with open(img_filepath, 'wb') as img_file:
                        img_file.write(img_response.content)

            logging.info(f"{len(image_urls)} images saved to {save_folder}")
            return image_urls

        except Exception as e:
            logging.error(f"Error during scrape_images: {e}")
            return []

    def scrape_links(self, elements=['a', 'area', 'link', 'img', 'iframe'], attributes=['href', 'src']):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = self._make_request(self.url, headers=headers)
            if not response:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for element in elements:
                for link_elem in soup.find_all(element):
                    for attribute in attributes:
                        link = link_elem.get(attribute)
                        if link:
                            links.append(link)

            return links

        except Exception as e:
            logging.error(f"Error during scrape_links: {e}")
            return []
