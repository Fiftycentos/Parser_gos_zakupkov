from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

import time
import random

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


HEADERS1 = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/533.28.5 (KHTML, like Gecko) Version/5.0.3 Safari/533.28.5'}
HEADERS2 = {'user-agent': 'Mozilla/5.0 (Windows 98) AppleWebKit/5360 (KHTML, like Gecko) Chrome/36.0.808.0 Mobile Safari/5360'}
HEADERS3 = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0) AppleWebKit/531.21.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.21.7'}
HEADERS4 = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/534.15.6 (KHTML, like Gecko) Version/4.0 Safari/534.15.6'}
HEADERS5 = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/531.46.3 (KHTML, like Gecko) Version/4.1 Safari/531.46.3'}
HEADERS6 = {'user-agent': 'Mozilla/5.0 (Windows NT 5.01; sl-SI; rv:1.9.2.20) Gecko/20130813 Firefox/37.0'}


mylist = [HEADERS1, HEADERS2, HEADERS3, HEADERS4, HEADERS5, HEADERS6]

MAIN_URL = 'https://www.goszakup.gov.kz/ru/registry/show_supplier/280311'

urls = pd.read_csv('urls.csv')


def get_html(url, hea, params=None):
    return requests.get(url, headers=hea, params=params, verify=False)


def parsing(url):
    soup = bs(url, "lxml")

    elements = soup.find_all('tr')

    data = {'Наименование организации': [],
            'БИН организации': [],
            'ФИО руководителя' : [],
            'ИИН руководителя' : [],
            'Полный адрес организации' : []
            }


    for element in elements:
        if element.find('th', text='Наименование на рус. языке'):
            name = element.find('th', text='Наименование на рус. языке').find_next_sibling('td').text
            data['Наименование организации'].append(name)

        if element.find('th', text='БИН участника'):
            bin = element.find('th', text='БИН участника').find_next_sibling('td').text
            data['БИН организации'].append(bin)

        if element.find('th', text='ФИО'):
            fio = element.find('th', text='ФИО').find_next_sibling('td').text
            data['ФИО руководителя'].append(fio)

        if element.find('th', text='ИИН'):
            iin = element.find('th', text='ИИН').find_next_sibling('td').text
            data['ИИН руководителя'].append(iin)
    try:
        if elements[-1]:
            data['Полный адрес организации'].append(elements[-1].text.strip().split('\n')[4].strip())
    except:
        print(None)
    return [data]


def start_parser(web):

    html = get_html(web, random.choice(mylist))

    if html.status_code == 200:
        data = []
        for url in urls['Url']:
            data.extend(parsing(get_html(url, random.choice(mylist)).text))
            time.sleep(2) # waiting for security

        return data
    else:
        return print(html.status_code, 'NONE')


df = pd.DataFrame(start_parser(MAIN_URL))

df = df[['Наименование организации', 'БИН организации','ФИО руководителя','ИИН руководителя','Полный адрес организации']]
df1 = df.drop(['Unnamed: 0'], axis=1)
df1 = df1.drop_duplicates()
name = 'data_file_test_last.csv'

df1.to_csv(name)