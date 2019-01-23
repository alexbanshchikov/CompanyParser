import requests
from bs4 import BeautifulSoup as bs
import time
import calendar

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

base_url = 'http://www.zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=7018007264&strictEqual=on&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&fz44=on&fz223=on&ppRf615=on&af=on&ca=on&pc=on&pa=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE'

def parse_zakupki(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        div1 = answer.find_all('div', attrs={'class':'registerBox registerBoxBank margBtm20'})
        print(len(div1))
    else:
        print('ERROR')

def parse_nalog(headers):
    nalog_url = 'https://rmsp.nalog.ru/search-proc.json?query=7021004633'
    session = requests.Session()
    request = session.get(nalog_url, headers=headers)
    if request.status_code == 200:
        '''answer = bs(request.content, 'html.parser')'''
        answer = request.json()
        ans = answer.pop('data')
        answer = ans[0]
        token = answer.pop('token')
        nalog_url_1 = 'https://egrul.nalog.ru/vyp-request/' + token + '?r=&_=' + str(int(time.time()*1000))
        headers = {'Accept': '*/*',
                   'Host': 'egrul.nalog.ru',
                   'Referer': 'https://egrul.nalog.ru/index.html',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                   }
        request1 = session.get(nalog_url_1, headers=headers)
        print(nalog_url_1)
        print(request1.cookies)
        nalog_url_2 = 'https://egrul.nalog.ru/vyp-status/' + token + '?r=' + str(int(time.time()*1000)-1) + '&_=' + str(int(time.time()*1000))
        request2 = session.get(nalog_url_2, headers=headers)
        if request1.status_code == 200:
            print('GOOD')
        else:
            print(request1.status_code)
        if request2.status_code == 200:
            print('GOOD')
        else:
            print(request2.status_code)
        nalog_url_3 = 'https://egrul.nalog.ru/vyp-download/' + token
        request3 = session.get(nalog_url_3, headers=headers)
        if request3.status_code == 200:
            print('GOOD')
        else:
            print(request3.status_code)
    else:
        print('ERROR')

'''parse_zakupki(base_url, headers)'''
parse_nalog(headers)