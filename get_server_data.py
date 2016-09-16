import requests
import bs4

def get_server_data(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    return soup
