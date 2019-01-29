import requests

base_url = 'http://www.zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=7018007264&strictEqual=on&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&fz44=on&fz223=on&ppRf615=on&af=on&ca=on&pc=on&pa=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE'

'''def parse_zakupki(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        answer = bs(request.content, 'html.parser')
        div1 = answer.find_all('div', attrs={'class':'registerBox registerBoxBank margBtm20'})
        print(len(div1))
    else:
        print('ERROR')
'''
def parse_nalog(inn):
    url = "https://rmsp.nalog.ru/search-proc.json"

    querystring = {"query": inn}

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    tokenOld = response.json().pop('data')[0].pop('token')

    url = "https://pb.nalog.ru/download-proc.json"              # По этому запросу получаешь токен для Прозрачного Бизнеса
    querystring = {"token": tokenOld, "inn": inn, "pdf": "vyp"}

    response = requests.request("POST", url, body=querystring)
    print(response.content)

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

def parse_nalog_second_step():
    url = "https://pb.nalog.ru/download-proc.json"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"params\"\r\n\r\ntoken=A6A58C340B10BBAC23C71BF238E3B8976D43D0D65124B7D18DB4D7692A9731C567AE3BF9F9B40C295F68C0FE01D412A8&inn=7021004633&pdf=vyp\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'Postman-Token': "93f28bb7-e6bf-4f91-88c8-f984a519ac9a"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

# parse_zakupki(base_url, headers)

#parse_nalog(7021004633)

def parse_nalog_third():
    url = "https://pb.nalog.ru/excerpt.pdf?token=CC5AE858100FB9D0FB9EFD7DF9FCC0D94323CC2CB91EC45DEFBB217768630D687A9DF6A09CF658303AB346B8301654BB61E04AFD3EE110AC708C1070B97137F9CC40374A9EE9152A07F0AA1AB5AD9A2ABE1A9BB98851AE16F8EC8D2A87EF41CA34F93B14BF8660A232309BDA33A704B69F61EF722A1F7EB1E15DBDF397EE4F65AA09AC45FAAEE25882FB55664504F9AEB9CD3C21D81998CBD894A348B3684565"

   # querystring = {
    #    "token": "CC5AE858100FB9D0FB9EFD7DF9FCC0D94323CC2CB91EC45DEFBB217768630D687A9DF6A09CF658303AB346B8301654BB61E04AFD3EE110AC708C1070B97137F9CC40374A9EE9152A07F0AA1AB5AD9A2ABE1A9BB98851AE16F8EC8D2A87EF41CA34F93B14BF8660A232309BDA33A704B69F61EF722A1F7EB1E15DBDF397EE4F65AA09AC45FAAEE25882FB55664504F9AEB9CD3C21D81998CBD894A348B3684565"}

    payload = ""
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "https://pb.nalog.ru/company.html?token=A6A58C340B10BBAC23C71BF238E3B8976D43D0D65124B7D18DB4D7692A9731C567AE3BF9F9B40C295F68C0FE01D412A8",
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

    response = requests.request("POST", url, data=payload, headers=headers)#, params=querystring)

    print(response.text)

#parse_nalog_second_step()
parse_nalog_third()