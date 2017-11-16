import requests
import click
from bs4 import BeautifulSoup as bs

def make_request(url):
    '''Makes a request to the passed url, returns a beautifulsoup object'''
    headers={'User-Agent':
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'} 
    requestpage = requests.get(url,headers = headers, timeout=15)
    if requestpage.status_code == 200:
        soup = bs(requestpage.text,'lxml')
    return soup

def return_num_items(url):
    '''Helper, Returns the number of items returned for a particular keyword
    http://www.shopping.com/products?KW=<keyword>'''
    try:
        soup = make_request(url)
        div = soup.find('div', {'id': "sortFiltersBox"}).find("span").get("name")
        num_items = int(div.split(':')[1])
        print(num_items)
    except AttributeError:
        #Call Logging function
        print("\n Attribute Error")
    except IndexError:
        print("\n Index Error")
    return num_items

def build_dict(product):
    temp = {}
    # Not Grabbing URLs to product images
    product_name = product.find("a", {"class":"productName"})
    if product_name:
        temp["Product Name"] = product_name.get("title")
        if not temp['Product Name']:
            temp["Product Name"]=product_name.find("span").get("title")
    product_price = product.find("span", {"class":"productPrice"})
    if product_price:
        temp["Product Price"] = product_price.get_text().strip()
    product_merchant = product.find("span", {"class":"newMerchantName"})
    
    if not product_merchant:
        product_merchant = product.find("a",{"class":"newMerchantName"})
    temp["Product Merchant"] = product_merchant.get_text().strip()
    
    product_url = product.find("div", {"class":["productGrid","gridItemTop"]})
    if product_url:
        p_url = product_url.find("a")
        if p_url:
            temp["Product URL"] = "http://www.shopping.com"+p_url.get("href")

    product_shipping = product.find("div",{"class":["taxShippingArea","freeShip"]})
    
    if product_shipping:
        temp["Product Shipping"] = product_shipping.get_text().strip()
    


    import pprint
    pprint.pprint(temp)
    return temp

def return_items(url):
    '''Helper, Returns a JSON file of the products returned on a particular
    page for a particular keyword'''
    soup = make_request(url)
    productdivs = soup.find_all("div", {"class": "gridBox"})
    list_of_products = [build_dict(product) for product in productdivs]
    return list_of_products

@click.command()
@click.argument('keyw', type=click.STRING, nargs =-1)
@click.option('--pg', type=click.STRING, default=None)
def entrypoint(keyw=None, pg=None):
    '''Entry Point for the program, makes request and calls respective helpers for query'''   
    if not keyw:
        print("No keyword supplied")
        return
    else:
        keyw = ' '.join(keyw)
    if pg:
        # Query 2 URL
        # Create different url
        url = "http://www.shopping.com/products~PG-<number>?KW="
        url = url.replace('<number>', pg)+keyw
        
        import pandas
        df = pandas.DataFrame(return_items(url))
        df.to_csv("Products.csv")

    else:
        #Query 1 URL
        url = 'http://www.shopping.com/products?sb=1&KW='+ keyw
        return_num_items(url)
        

if __name__ == "__main__":
    entrypoint()
