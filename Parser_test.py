from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


HEADERS6 = {'user-agent': 'Mozilla/5.0 (Windows NT 5.01; sl-SI; rv:1.9.2.20) Gecko/20130813 Firefox/37.0'}

MAIN_URL = 'https://www.goszakup.gov.kz/ru/registry/rqc?count_record=50&page='


def get_html(url, hea, params=None):

    return requests.get(url, headers=hea, params=params, verify=False)

def parsing(url):

    soup = bs(url, "lxml")

    elements = soup.find_all('td')
    data = []
    for element in elements:
        if element.find('a', href=True):
            url_url = element.find('a', href=True)['href']
            data.append(
            {
            'Url': url_url
            })
    return data


def start_parser(web, hea):
    html = get_html(web, hea)

    if html.status_code == 200:
        data = []
        for i in range(1, 11):
            url = f'{web}' + f'{i}'
            data.extend(parsing(get_html(url, hea).text))

        return data
    else:
        return print(html.status_code, ' NONE')

print(start_parser(MAIN_URL, HEADERS6))

df = pd.DataFrame(start_parser(MAIN_URL, HEADERS6))
name = 'urls.csv'
df.to_csv(name)
