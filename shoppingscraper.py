import requests
import click
from bs4 import BeautifulSoup as bs

def make_request(url):
    '''Makes a request to the passed url, returns a beautifulsoup object'''

def return_num_items(soup):
    '''Helper, Returns the number of items returned for a particular keyword
    http://www.shopping.com/products?KW=<keyword>'''
    try:
        div = soup.find('div',{'id': "sortFiltersBox"}).find("span").get("name")
        print(div.split(':')[1])
    except AttributeError:
        #Call Logging function
        print("\n Attribute Error")
    except IndexError:
        print("\n Index Error")
    
    return

def return_items(soup):
    '''Helper, Returns a JSON file of the products returned on a particular page for a particular keyword'''
    return

@click.command()
@click.argument('keyw',type=click.STRING,nargs =-1)
@click.option('--pg',type=click.STRING,default=None)
def entrypoint(keyw = None,pg=None):
    '''Entry Point for the program, makes request and calls respective helpers for query '''
    
    if not keyw:
        print("No keyword supplied")
        return
    else:
        keyw = ' '.join(keyw)
    if pg:
        # Query 2 URL
        # Create different url
        url = "http://www.shopping.com/products~PG-<number>?KW=".replace('<number>',pg)+keyw
        print(url)
    else:
        #Query 1 URL
        url = 'http://www.shopping.com/products?sb=1&KW='+ keyw
    
    headers={'User-Agent':
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'} 
    requestpage = requests.get(url,headers = headers, timeout=15)
    if requestpage.status_code == 200:
        soup = bs(requestpage.text,'lxml')
        return_num_items(soup)
    else:
        print("\n Something went wrong")

if __name__ == "__main__":
    entrypoint()
