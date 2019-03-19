import requests
from bs4 import BeautifulSoup as bs
import os
import time
import docx2txt
import chardet
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO
from io import BytesIO
from bs4 import BeautifulSoup as bs
from tabula import read_pdf
import pandas as pd

def parse_zakupki(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')

        dict = {'info': None, 'timeNews': None, 'zayavka_po': None, 'first_price': None, 'currency': None,
                'URL': None, 'n1': None,
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

            number_req = div1.find('td', class_='descriptTenderTd').find('a', target='_blank').get('href')
            if number_req.find('http') == -1:
                dict['URL'] = 'http://www.zakupki.gov.ru' + number_req  #URL закупки
            else:
                dict['URL'] = number_req #URL закупки
            number = number_req.find('=')
            dict['n1'] = number_req[number + 1:]  # номер закупки

            try:
                buf = div1.find('dd', class_='nameOrganization').find('a', target='_blank')
                dict['customer'] = buf.text.strip()   #Наименование организации
                dict['customer_URL'] = buf.get('href')    #Ссылка на организацию
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

def parse_pdf(path_to_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    # retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path_to_file, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def deep_search(headers, base_url, args):
    response = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        for div1 in answer.find_all('div', attrs={'class': 'registerBox registerBoxBank margBtm20'}):
            number_zayavki = div1.find('span', attrs={'class': 'orange'}).text  # тип заявки
            number_req = div1.find('td', class_='descriptTenderTd').find('a', target='_blank').get('href')
            if number_req.find('http') == -1:
                number = number_req.find('=')
                n1 = number_req[number+1:]        # номер закупки
            else:
                number = number_req.find('=')
                n1 = number_req[number + 1:]      # номер закупки
            if '223' in number_zayavki:
                URL = 'http://zakupki.gov.ru/223/purchase/public/purchase/info/documents.html?regNumber=' + n1
            else:
                URL = 'http://www.zakupki.gov.ru/epz/order/notice/ea44/view/documents.html?regNumber=' + n1
            list = documents_zakupki(headers, URL)
            print(list)
            buf = ''
            for i in range(len(list)):
                req = session.get(list[i], headers=headers)
                print(list[i])
                if 'notice' in list[i]:
                    buf = buf + req.content.decode('utf-8')
                    if buf.find(args) is not None:
                        response.append(number_zayavki)
                        break

                if 'download' in list[i]:
                    print(req.content[1:20])
                    if b'\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00`' in req.content[1:40]:  # EXCEL
                        print('excel')
                        name = 'D://kek' + str(i) + '.xlsx'
                        file = open(name, 'wb')       # создаем файл для записи результатов
                        file.write(req.content)       # записываем результат
                        file.close()                  # закрываем файл''
                        text = pd.read_excel(r'name')
                        os.remove(name)
                        if text.find(args) is not None:
                            response.append(number_zayavki)
                        else:
                            break

                    if b'\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00' in req.content[1:40]:   # WORD
                        name = 'D://kek' + str(i) + '.docx'
                        file = open(name, 'wb')        # создаем файл для записи результатов
                        file.write(req.content)        # записываем результат
                        file.close()                   # закрываем файл
                        text = docx2txt.process(name)
                        os.remove(name)
                        if text.find(args) is not None:
                            response.append(number_zayavki)
                        else:
                            break

                    if b'PDF' in req.content[1:5]:                                              # PDF
                        name = 'D://alarm' + str(i) + '.pdf'
                        file = open(name, 'wb')        # создаем файл для записи результатов
                        file.write(req.content)        # записываем результат
                        file.close()                   # закрываем файл
                        text = parse_pdf(name)
                        os.remove(name)
                        if text.find(args) is not None:
                            response.append(number_zayavki)
                        else:
                            break

                    if b'\xcf\x11' in req.content[1:10]:
                        print('doc or xls, we\'re sorry guys')
        return response
    else:
        print('ERROR')

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
parse_zakupki(base_url, headers) # получение списка всех закупок на странице

base_url = 'http://www.zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=0873200001718000443'
#base_url = 'http://www.zakupki.gov.ru/epz/order/notice/ep44/view/common-info.html?regNumber=0348100009118000197'
#infa_about_zakupka(base_url, headers) #подробная информация о закупке

#base_url = 'http://www.zakupki.gov.ru/epz/order/notice/ea44/view/documents.html?regNumber=0873200001718000443'
base_url = 'http://zakupki.gov.ru/223/purchase/public/purchase/info/documents.html?regNumber=31807203209'
#documents_zakupki(headers, base_url) #получение всех документов о закупке

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

base_url = 'http://www.zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%BE%D0%B5+%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5&morphology=on&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=true&fz44=on&fz223=on&ppRf615=on&fz94=on&af=on&ca=on&pc=on&pa=on&priceFrom=0&priceTo=100000000&currencyId=1&region_regions_5277365=region_regions_5277365&region_regions_5277335=region_regions_5277335&regions=5277365%2C5277335&regionDeleted=false&publishDateFrom=01.11.2018&publishDateTo=20.02.2019&updateDateFrom=03.10.2018&updateDateTo=10.01.2019&sortBy=UPDATE_DATE'
#deep_search(headers, base_url)

typeRequest = 'morphology=on' #поиск с учетом всех форм слов
typeRequest = 'strictEqual=false' #строгое соответствие

service = 'openMode=USE_DEFAULT_PARAMS&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false'
typePurchases = 'fz44=on&fz223=on&ppRf615=on&fz94=on' # закупки по конкретным ФЗ
stage = 'af=on&ca=on&pc=on&pa=on' # подача заявок, работа комиссии, процедура завершена, процедура отменена

way = 'placingWaysList=OK504'# способ определения поставщика: конкурс в электронной форме
way = 'placingWaysList=OK504%2CZK504%2CZP504%2COKU504%2COKD504%2CKESMBO%2CAESMBO%2CZKESMBO%2CZPESMBO%2CEA94%2CEA%' \
      '2CEP%2CPO%2CPO44%2CEA615%2CPO615%2CZKK44%2COKU44%2CZP44%2CZKB44%2CZK44%2CZK%2CTB%2CES%2CZH%2CEP44%2COKD44%2CZA44%' \
      '2CSZ%2CEF%2COK44%2COK%2CEA44%2CZKKU44%2COA%2CZKKD44%2CINM111%2CPR'
# Открытый конкурс в электронной форме - OK504
# Запрос котировок в электронной форме - ZK504
# Запрос предложений в электронной форме - ZP504
# Конкурс с ограниченным участием в электронной форме - OKU504
# Двухэтапный конкурс в электронной форме - OKD504
# Конкурс в электронной форме, участниками которого могут являться только субъекты малого и среднего предпринимательства - KESMBO
# Аукцион в электронной форме, участниками которого могут являться только субъекты малого и среднего предпринимательства - AESMBO
# Запрос котировок в электронной форме, участниками которого могут являться только субъекты малого и среднего предпринимательства - ZKESMBO
# Запрос предложений в электронной форме, участниками которого могут являться только субъекты малого и среднего предпринимательства - ZPESMBO
# Открытый аукцион в электронной форме (по 94ФЗ) - EA94
# Открытый аукцион в электронной форме - EA
# Закупка у единственного поставщика (исполнителя, подрядчика) - EP
# Предварительный отбор - PO
# Предварительный отбор - PO44
# Электронный аукцион на оказание услуг или выполнение работ по капитальному ремонту общего имущества в многоквартирном доме - EA615
# Предварительный отбор квалифицированных подрядных организаций - PO615
# Закрытый конкурс - ZKK44
# Конкурс с ограниченным участием - OKU44
# Запрос предложений - ZP44
# Запрос котировок без размещения извещения - ZKB44
# Запрос котировок - ZK44
# Запрос котировок - ZK
# Торги на товарных биржах - TB
# Единственный поставщик - ES
# Результат рассмотрения и оценки котировочных заявок (Глава 5 Федерального закона №94-Ф3) - ZH
# Закупка у единственного поставщика (подрядчика, исполнителя) - EP44
# Двухэтапный конкурс - OKD44
# Закрытый аукцион - ZA44
# Сообщение о заинтересованности в проведении открытого конкурса - SZ
# Открытый аукцион в электронной форме - EF
# Открытый конкурс - OK44
# Открытый конкурс - OK
# Электронный аукцион - EA44
# Закрытый конкурс с ограниченным участием - ZKKU44
# Открытый аукцион - OA
# Закрытый двухэтапный конкурс - ZKKD44
# Способ определения поставщика (подрядчика, исполнителя), установленный Правительством Российской Федерации в соответствии со ст. 111 Федерального закона № 44-ФЗ - INM111
# Прочее - PR

price = 'priceFromGeneral=14&priceToGeneral=1000000' #начальная цена от и до
participantName = 'participantName=мука' #участник закупки
publishedData = 'publishDateFrom=01.03.2019&publishDateTo=17.03.2019' # дата публикации от и до
updateDate = 'updateDateFrom=01.03.2019&updateDateTo=17.03.2019' #дата обновления от и до
levelOfOrganization = 'F=on&S=on&M=on' #уровень: федеральный, субъект РФ, муниципальный

district = 'is_volga_district=1&is_far_eastern_district=1&is_north_west_district=1&districts=5277399%2C5277362%2C5277336'
# district = 'is_far_eastern_district=1&districts=5277399' #федеральный уровень заказчика: Дальневосточный ФО
# district = 'is_volga_district=1&districts=5277362' #федеральный уровень заказчика: Приволжский ФО
# district = 'is_north_west_district=1&districts=527733' #федеральный уровень заказчика: Северо-Западный ФО
# district = 'is_north_caucasus_district=1&districts=9409197' #федеральный уровень заказчика: Северо-Кавказский ФО
# district = 'is_siberian_district=1&districts=5277384' #федеральный уровень заказчика: Сибирский ФО
# district = 'is_ural_district=1&districts=5277377' #федеральный уровень заказчика: Уральский ФО
# district = 'is_central_district=1&districts=5277317' #федеральный уровень заказчика: Центральный ФО
# district = 'is_southern_district=1&districts=9371527' #федеральный уровень заказчика: Южный ФО

deliveryAdress = 'deliveryAddress=ленина' #адрес места поставки
applSubmissionDate = 'applSubmissionCloseDateFrom=01.03.2019&applSubmissionCloseDateTo=05.03.2019' #дата окончания подачи заявок
exclText = 'exclText=баранки' #исключить слово