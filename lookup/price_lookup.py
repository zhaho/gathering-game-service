""" Module for checking prices of a game object """

import urllib
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def game_title(g_title):
    """ Function for retrieving price based on game title """
    title_found = False
    encode_url = urllib.parse.quote(g_title)
    url = os.getenv("PRICE_LOOKUP_URL") + encode_url

    web_url = urllib.request.urlopen(url)

    data = web_url.read().decode("utf-8")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(data, 'html.parser')

    # Find the specific information you need
    item_div = soup.find('div', class_='searchcell divider itemname')
    if item_div:
        title_element = item_div.find('span', class_='name')
        if title_element:
            title = title_element.find('a').text.strip()
            if title == g_title:
                title_found = True

    if title_found:
        item_div = soup.find('div', class_='searchcell bestprice multibestprice')
        if item_div:
            price_element = item_div.find('span', class_='price')
            if price_element:
                price = price_element.text.strip()[4:]

                # Split the price by comma
                price_parts = price.split(',')
                price = ''.join(price_parts[:1])

                # Split the price string by dots
                price_parts = price.split('.')
                price = ''.join(price_parts[:2])

                return int(price)

    return None
