import requests
from bs4 import BeautifulSoup as bs
import os
import time
import docx2txt
#import chardet

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

base_url = 'http://www.zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%BC%D1%83%D0%BA%D0%B0&' \
           'morphology=on&' \
           'pageNumber=1&' \
           'sortDirection=false&recordsPerPage=_50&' \
           'showLotsInfoHidden=true&' \
           'fz44=on&' \
           'fz223=on&' \
           'ppRf615=on&' \
           'fz94=on&' \
           'af=on&' \
           'ca=on&' \
           'pc=on&' \
           'pa=on&' \
           'priceFrom=0&' \
           'priceTo=100000000&' \
           'currencyId=1&' \
           'region_regions_5277365=region_regions_5277365&region_regions_5277335=region_regions_5277335&' \
           'regions=5277365%2C5277335&' \
           'regionDeleted=false&' \
           'publishDateFrom=01.11.2018&' \
           'publishDateTo=20.02.2019&' \
           'updateDateFrom=03.10.2018&' \
           'updateDateTo=10.01.2019&' \
           'sortBy=UPDATE_DATE'

def parse_zakupki(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        dict = {'info': None, 'timeNews': None, 'zayavka_po': None, 'first_price': None, 'currency': None,
                'price': None, 'URL': None, 'n1': None,
                'customer': None, 'customer_URL': None, 'describe': None, 'identification_code': None,
                'posted': None, 'updated': None}
        for div1 in answer.find_all('div', attrs={'class': 'registerBox registerBoxBank margBtm20'}):
            dict['info'] = div1.find('strong').text.strip()
            dict['timeNews'] = div1.find('span').text.strip().split('/')[0]
            dict['zayavka_po'] = div1.find('span', attrs={'class': 'orange'}).text  #тип заявки

            try:
                dict['first_price'] = div1.find_all('strong')[1].text.strip().split(',')[0].strip() + ',' + div1.find_all('strong')[1].text.strip().split(',')[1].strip()
            except:
                pass
            try:
                dict['currency'] = div1.find('span', attrs={'class': 'currency'}).text
            except:
                pass
            try:
                dict['price'] = (''.join(str(first_price[0]).strip().split()), str(first_price[1]), currency) # цена
            except:
                pass

            number_req = div1.find('td', class_='descriptTenderTd').find('a', target='_blank').get('href')
            if number_req.find('http') == -1:
                dict['URL'] = 'http://www.zakupki.gov.ru' + number_req  #URL закупки
                number = number_req.find('=')
                dict['n1'] = number_req[number+1:]        #номер закупки
            else:
                dict['URL'] = number_req #URL закупки
                number = number_req.find('=')
                dict['n1'] = number_req[number + 1:]  # номер закупки

            try:
                dict['customer'] = div1.find('dd', class_='nameOrganization').find('a', target='_blank').text.strip()   #Наименование организации
                dict['customer_URL'] = div1.find('dd', class_='nameOrganization').find('a', target='_blank').get('href')    #Ссылка на организацию
                if number_req.find('http') == -1:
                    dict['customer_URL'] = 'http://www.zakupki.gov.ru' + dict['customer_URL']
            except:
                pass

            dict['describe'] = div1.find('td', class_='descriptTenderTd').find_all('dd')[1].text.strip()

            try:
                dict['identification_code'] = div1.find('dd', class_='padTop10').find('dl').text.strip()
            except:
                pass

            dict['posted'] = div1.find('td', class_='amountTenderTd').find('li').text.strip()
            dict['updated'] = div1.find('td', class_='amountTenderTd').find_all('li')[1].text.strip()

            print(dict)
            print('')

    else:
        print('ERROR')

#parse_zakupki(base_url, headers)

base_url = 'http://www.zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=0873200001718000443'
#base_url = 'http://www.zakupki.gov.ru/epz/order/notice/ep44/view/common-info.html?regNumber=0348100009118000197'

def infa_about_zakupka(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        HEAD = answer.find_all('h2')
        head = 0
        for div in answer.find_all('div', class_='noticeTabBoxWrapper'):
            print(HEAD[head].text)
            for div1 in div.find_all('table'):
                for div11 in div1.find_all('tr'):
                    data = div11.find_all('td')
                    if len(data) == 2:
                        first = data[0].text.strip()
                        second = data[1].text.strip()
                        #number = first.find('\n')
                        #if number != -1:
                        #    first = str(first[:number]).strip() + str(first[number+1:]).strip()
                        #number = second.find('\n')
                        #if number != -1:
                         #   second = str(second[:number]).strip() + str(second[number + 1:]).strip()
                        print(first)
                        print(second)
                        print('')
                    else:
                        print(data[0].text.strip())
                        print('')
            head += 1
    else:
        print('ERROR')

#infa_about_zakupka(base_url, headers)

#base_url = 'http://www.zakupki.gov.ru/epz/order/notice/ea44/view/documents.html?regNumber=0873200001718000443'
base_url = 'http://zakupki.gov.ru/223/purchase/public/purchase/info/documents.html?regNumber=31807203209'

def documents_zakupki(headers, base_url):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        list = []
        if '/ea44/' in base_url:
            for div in answer.find_all('a', class_=''):
                if 'http' in div.get('href'):
                    #print(div.get('href'))
                    list.append(div.get('href'))
                if '/epz/order' in div.get('href'):
                    #print('http://zakupki.gov.ru' + div.get('href'))
                    list.append('http://zakupki.gov.ru' + div.get('href'))
        if '/223/' in base_url:
            for div in answer.find_all('a', class_='epz_aware'):
                #print('http://zakupki.gov.ru' + div.get('href'))
                list.append('http://zakupki.gov.ru' + div.get('href'))
        return list
    else:
        print('ERROR')
        return 0

#documents_zakupki(headers, base_url)

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

base_url = 'http://www.zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%BE%D0%B5+%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5&morphology=on&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=true&fz44=on&fz223=on&ppRf615=on&fz94=on&af=on&ca=on&pc=on&pa=on&priceFrom=0&priceTo=100000000&currencyId=1&region_regions_5277365=region_regions_5277365&region_regions_5277335=region_regions_5277335&regions=5277365%2C5277335&regionDeleted=false&publishDateFrom=01.11.2018&publishDateTo=20.02.2019&updateDateFrom=03.10.2018&updateDateTo=10.01.2019&sortBy=UPDATE_DATE'

def deep_search(headers, base_url):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        for div1 in answer.find_all('div', attrs={'class': 'registerBox registerBoxBank margBtm20'}):
            number_zayavki = div1.find('span', attrs={'class': 'orange'}).text  # тип заявки
            number_req = div1.find('td', class_='descriptTenderTd').find('a', target='_blank').get('href')
            if number_req.find('http') == -1:
                number = number_req.find('=')
                n1 = number_req[number+1:]        #номер закупки
            else:
                number = number_req.find('=')
                n1 = number_req[number + 1:]  # номер закупки
            if '223' in number_zayavki:
                URL = 'http://zakupki.gov.ru/223/purchase/public/purchase/info/documents.html?regNumber=' + n1
            else:
                URL = 'http://www.zakupki.gov.ru/epz/order/notice/ea44/view/documents.html?regNumber=' + n1
            list = documents_zakupki(headers, URL)
            #print(list)
            buf = ''
            for i in range(len(list)):
                req = session.get(list[i], headers=headers)
                if 'notice' in list[i]:
                    #print(req.content.decode('utf-8'))
                    buf = buf + req.content.decode('utf-8')
                if 'download' in list[i]:
                    print(req.content[1:20])
                    if b'PK\x03\x04\x14\x00\x06\x00' in req.content and b'xcf\x11' not in req.content:
                        #print(chardet.detect(req.content))
                        #print(req.content.decode('utf-8').find('Цена'.encode('utf-8')))

                        name = 'D://kek' + str(i) + '.docx'
                        file = open(name, 'wb')  # создаем файл для записи результатов
                        file.write(req.content)  # записываем результат
                        file.close()  # закрываем файл''
                        print('excellent')
                        text = docx2txt.process(name)
                        #print(text)
                        os.remove(name)

            #print(buf.find('Недятько')) - поиск в протоколах и извещениях
            #print(text.find(smth)) - поиск в doc документах
    else:
        print('ERROR')
#start_time = time.time()
deep_search(headers, base_url)
#print("--- %s seconds ---" % (time.time() - start_time))
