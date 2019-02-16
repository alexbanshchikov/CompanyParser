import requests
from bs4 import BeautifulSoup as bs

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
        for div1 in answer.find_all('div', attrs={'class': 'registerBox registerBoxBank margBtm20'}):
            info = div1.find('strong').text.strip()
            timeNews = div1.find('span').text.strip().split('/')[0]
            zayavka_po = div1.find('span', attrs={'class': 'orange'}).text  #тип заявки

            first_price = div1.find_all('strong')[1].text.strip().split(',')
            currency = div1.find('span', attrs={'class': 'currency'}).text
            price = (''.join(str(first_price[0]).strip().split()), str(first_price[1]), currency) # цена

            number_req = div1.find('td', class_='descriptTenderTd').find('a', target='_blank').get('href')
            if number_req.find('http') == -1:
                url = 'http://www.zakupki.gov.ru' + number_req  #URL закупки
                number = number_req.find('=')
                n1 = number_req[number+1:]        #номер закупки
            else:
                url = number_req #URL закупки
                number = number_req.find('=')
                n1 = number_req[number + 1:]  # номер закупки

            try:
                customer = div1.find('dd', class_='nameOrganization').find('a', target='_blank').text.strip()   #Наименование организации
                customer_url = div1.find('dd', class_='nameOrganization').find('a', target='_blank').get('href')    #Ссылка на организацию
                if number_req.find('http') == -1:
                    customer_url = 'http://www.zakupki.gov.ru' + customer_url
            except:
                customer = None
                customer_url = None

            describe = div1.find('td', class_='descriptTenderTd').find_all('dd')[1].text.strip()

            try:
                identification_code = div1.find('dd', class_='padTop10').find('dl').text.strip()
            except:
                identification_code = None

            posted = div1.find('td', class_='amountTenderTd').find('li').text.strip()
            updated = div1.find('td', class_='amountTenderTd').find_all('li')[1].text.strip()

            print(info, timeNews, zayavka_po, price, '\n', url, '\n', n1, customer, '\n', customer_url, '\n', describe, identification_code, '\n', posted, updated)

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
        if '/ea44/' in base_url:
            for div in answer.find_all('a', class_=''):
                if 'http' in div.get('href'):
                    print(div.get('href'))
                if '/epz/order' in div.get('href'):
                    print('http://zakupki.gov.ru' + div.get('href'))
        if '/223/' in base_url:
            for div in answer.find_all('a', class_='epz_aware'):
                print('http://zakupki.gov.ru' + div.get('href'))
    else:
        print('ERROR')

documents_zakupki(headers, base_url)