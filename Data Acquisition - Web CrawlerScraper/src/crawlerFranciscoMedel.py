"""
Author: Francisco Medel Molinero
Description of the crawler: The function of this script consist on crawl data from the web page(https://casika.es), getting the products, reference, description, current price and the discount of the products in x pages defined in the parameter of the function and store that information in a json file.
Input of the function: the max num of pages that we want to crawl of the website.
Output of the function: after running the script we will get a json file with the name of the products, url, description, current price and the discount of the product
"""

# Imports
import json
import requests
from bs4 import BeautifulSoup


# Definition fo the main function
def trade_spider(max_pages):
    # We define that we want to start crawling in the first page of the website
    page = 1
    f = open('data.json', 'w')

    # Dictionary to save the producto with its features
    dictionary = {}
    # list to add the features of the product
    lista = []

    while page <= max_pages:
        url = 'https://casika.es/muebles/?page=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")

        # We use this loop to get all the products in the page
        for link in soup.find_all('a', {'class': 'product_name'}):
            href = link.get('href')

            # Product reference(url of the specific product)
            lista.append(href)

            # We call this function to get data of the specific product
            get_single_item_item_data(href, f, lista)
            dictionary[link.string] = lista

            # Saving the values of the dictionary in the json file
            json.dump(dictionary, f)
            lista.clear()
            dictionary.clear()

        page += 1


# This function extracts specific of the url of the product
def get_single_item_item_data(item_url, f, lista):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for item_name in soup.find_all('div', {'class': 'product-description-short'}):
        # Item description
        lista.append(item_name.string)
        # json.dump(item_name.string, f)

    for div in soup.select('div.current-price'):
        for span in div.select('span'):
            # Item price & discount
            lista.append(span.text)


trade_spider(10)
