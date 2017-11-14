import requests
from bs4 import BeautifulSoup as bs

def return_num_items(soup):
    '''Helper, Returns the number of items returned for a particular keyword'''
    '''http://www.shopping.com/products?KW=<keyword>'''
    try:
        div = soup.find('div',{'id': "sortFiltersBox"}).find("span").get("name")
        print(div.split(':')[1])
    except AttributeError:
        #Call Logging function
        pass
    except IndexError:
        pass

def return_items(soup):
    '''Helper, Returns a JSON file of the products returned on a particular page for a particular keyword'''
    return


def entrypoint():
    url = 'http://www.shopping.com/products?sb=1&KW=~1231231'
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'} 
    requestpage = requests.get(url,headers = headers, timeout=15)
    soup = bs(requestpage.text,'lxml')
    return_num_items(soup)

if __name__ == "__main__":
    entrypoint()
