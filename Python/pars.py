import requests
import time

def parse_nalog(inn):
    url = "https://pb.nalog.ru/search-proc.json"

    querystring = {"query": inn}

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    tokenOld = response.json().pop('cmp').pop('data')[0].pop('token')

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

    file = open('D://test_content2.pdf', 'wb')  # создаем файл для записи результатов
    file.write(response.content)  # записываем результат
    file.close()  # закрываем файл'''

tokenOld = parse_nalog(7021004633)
tokenBig = parse_nalog_second_step(7021004633, tokenOld)
parse_nalog_third(tokenBig)



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

#Ex(tokenOld)