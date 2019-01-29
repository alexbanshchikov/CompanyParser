import requests
import time

def parse_nalog(inn):
    url = "https://rmsp.nalog.ru/search-proc.json"

    querystring = {"query": inn}

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    tokenOld = response.json().pop('data')[0].pop('token')
                                                                # Ниже нужно сделать GET запрос с новым токеном и также скачать pdf
    '''url = "https://pb.nalog.ru/excerpt.pdf"

    querystring = {"token": str(token)}

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    file = open('D://test_content2.pdf', 'wb')  # создаем файл для записи результатов
    file.write(response.content)  # записываем результат
    file.close()  # закрываем файл'''
    return str(tokenOld)

def parse_nalog_second_step(inn, tokenOld):
    url = "https://pb.nalog.ru/download-proc.json"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"params\"\r\n\r\ntoken=" + tokenOld + "&inn=" + str(inn) +"&pdf=vyp\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.json())
    print(response.json()['token'])
    return str(response.json()['token'])

def parse_nalog_third(tokenOld, tokenBig):
    url = "https://pb.nalog.ru/excerpt.pdf?token=" + tokenBig

    querystring = {
        "token": tokenBig}

    payload = ""
    headers = {
        'Referer': "https://pb.nalog.ru/company.html?token=" + tokenOld,
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cache-Control': "max-age=0",
        'Connection': "keep-alive",
        'Content-Length': "0",
        'Host': "pb.nalog.ru",
        'Origin': "https://pb.nalog.ru",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, headers=headers,  params=querystring)

    print(response.text)

tokenOld = parse_nalog(7021004633)
#tokenBig = parse_nalog_second_step(7021004633, tokenOld)
#parse_nalog_third(tokenOld, tokenBig)

def Ex(tokenOld):
    time1 = str(int(time.time()*1000))
    url = 'https://egrul.nalog.ru/vyp-request/' + tokenOld + '?r=&_=' + time1

    headers = {
        'cache-control': "no-cache",
    }
    querystring = {
        'r':'',
        '_': time1
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

Ex(tokenOld)