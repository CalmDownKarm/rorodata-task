'''
Simple Web Scraper for Shopping.com products, requires
Requests, Click, Json and beautifulsoup
Usage use --pg flag to give a pagenumber for query 2.
This is so that you can have multiple word search terms 
'''

import json
import requests
import click
from bs4 import BeautifulSoup as bs


def make_request(url):
    '''Makes a request to the passed url, returns a beautifulsoup object'''
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}
    try:
        requestpage = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.RequestException as request_er:
        print(request_er)
        return
    if requestpage.status_code == 200:
        soup = bs(requestpage.text, 'lxml')
        return soup


def return_num_items(url):
    '''Helper, Returns the number of items returned for a particular keyword
    http://www.shopping.com/products?KW=<keyword>'''
    try:
        soup = make_request(url)
        if not soup:
            return
        div = soup.find('div', {'id': "sortFiltersBox"})\
            .find("span").get("name")
        num_items = int(div.split(':')[1])
        print(repr(num_items) + " Total Items")
    except AttributeError:
        print("Please check Keyword")
        return
    except IndexError: #Incase some page doesn't print it seperated by a :
        print(div)
        return div
    return num_items


def build_dict(product):
    '''Builds a dictionary given an html div as a soup object'''
    temp = {}
    # Not Grabbing URLs to product images
    product_name = product.find("a", {"class": "productName"})
    if product_name:
        temp["Product Name"] = product_name.get("title")
        if not temp['Product Name']:
            temp["Product Name"] = product_name.find("span").get("title")
    
    product_price = product.find("span", {"class": "productPrice"})
    if product_price:
        temp["Product Price"] = product_price.get_text().strip()
    
    product_merchant = product.find("span", {"class": "newMerchantName"})
    if not product_merchant:
        product_merchant = product.find("a", {"class": "newMerchantName"})
    temp["Product Merchant"] = product_merchant.get_text().strip()
    
    product_url = product.find(
        "div", {"class": ["productGrid", "gridItemTop"]})
    if product_url:
        p_url = product_url.find("a")
        if p_url:
            temp["Product URL"] = "http://www.shopping.com" + p_url.get("href")
    
    product_shipping = product.find(
        "div", {"class": ["taxShippingArea", "freeShip"]})
    if product_shipping:
        temp["Product Shipping"] = product_shipping.get_text().strip()
    
    return temp


def return_items(url, pg, num_items):
    '''Helper, Returns a JSON file of the products returned on a particular
    page for a particular keyword'''
    max_num = int(num_items / 40) + 1
    if pg > max_num or pg <= 0:
        print("Page Number Range Should be 1 to " + repr(max_num))
        return
    soup = make_request(url)
    if not soup:
        return
    productdivs = soup.find_all("div", {"class": "gridBox"})
    list_of_products = [build_dict(product) for product in productdivs]
    print(repr(len(list_of_products)) + " Items returned")
    return list_of_products


@click.command()
@click.argument('keyw', type=click.STRING, nargs=-1)
@click.option('--pg', type=click.STRING, default=None)
def entrypoint(keyw=None, pg=None):
    '''Scraper For Shopping.com, use the --pg flag to enter page number'''
    if not keyw:
        print("No keyword supplied")
        return
    else:
        # Multi Keyword Argument comes as a tuple, need to cast to string
        keyw = ' '.join(keyw)
    url = 'http://www.shopping.com/products?sb=1&KW=' + keyw
    num_items = return_num_items(url)
    if not pg:
        return
    # Query 2 URL
    url = "http://www.shopping.com/products~PG-<number>?KW="
    url = url.replace('<number>', str(pg)) + keyw
    pg = int(round(float(pg)))
    listofproducts = return_items(url, pg, num_items)
    if not listofproducts:
        print("No Items Returned, please check Keywords/Page Numbers")
    else:
        with open("products.json", mode='w') as fileout:
            json.dump(listofproducts, fileout)


if __name__ == "__main__":
    entrypoint()
