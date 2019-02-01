import requests
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO
from io import BytesIO
from bs4 import BeautifulSoup as bs
from tabula import read_pdf
import pandas

def parse_nalog(inn):
    url = "https://pb.nalog.ru/search-proc.json"

    querystring = {"query": inn}

    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    tokenOld = response.json().pop('cmp').pop('data')[0].pop('token') #токен для получения выписки

    url = "https://rmsp.nalog.ru/search-proc.json"
    querystring = {"query": inn}
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    token = response.json().pop('data')[0].pop('token')

    url = "https://rmsp.nalog.ru/excerpt.pdf"
    querystring = {"token": str(token)}
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    file = open('D://reestr.pdf', 'wb')  # создаем файл для записи результатов
    file.write(response.content)  # записываем результат
    file.close()  # закрываем файл

    return str(tokenOld)

def parse_nalog_second_step(inn, tokenOld):
    url = "https://pb.nalog.ru/download-proc.json"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"params\"\r\n\r\ntoken=" + tokenOld + "&inn=" + str(inn) +"&pdf=vyp\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return str(response.json()['token'])

def parse_nalog_third(tokenBig):
    url = "https://pb.nalog.ru/excerpt.pdf"

    querystring = {
        "token": tokenBig
    }

    response = requests.request("POST", url, params=querystring)

    file = open('D://vypiska.pdf', 'wb')  # создаем файл для записи результатов
    file.write(response.content)  # записываем результат
    file.close()  # закрываем файл'''

#tokenOld = parse_nalog(7021004633)
#tokenBig = parse_nalog_second_step(7021004633, tokenOld)
#parse_nalog_third(tokenBig)

def parse_pdf(path_to_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    #retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    #device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
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

#text = parse_pdf('D://vypiska.pdf')

files = "vypiska.pdf"
path = 'D://vypiska.pdf'
df = read_pdf(path, multiple_tables=True, encoding='utf-8', spreadsheet=True)#, pages='all')#, spreadsheet=True)
print(df[1].iloc[8][1])
print(df[1].iloc[8][2])
#example = df[0]
#print(example.values)