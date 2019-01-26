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
    token = response.json().pop('data')[0].pop('token')
    print(token)
    url = "https://rmsp.nalog.ru/excerpt.pdf"

    querystring = {"token": str(token)}

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    file = open('D://test_content2.pdf', 'wb')  # создаем файл для записи результатов
    file.write(response.content)  # записываем результат
    file.close()  # закрываем файл

# parse_zakupki(base_url, headers)

parse_nalog(7021004633)
