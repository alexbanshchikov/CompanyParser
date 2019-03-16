import requests
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

def parse_pdf():
    path = 'D://vypiska.pdf'

    df = read_pdf(path, multiple_tables=True, encoding='utf-8', spreadsheet=True,
                  pages='1-2')  # , pages='all')#, spreadsheet=True)
    # print(df[1].iloc[8][1])
    # print(df[1].iloc[8][2])
    # print(df[1].iloc[3][2])
    dict = {}
    person = {}
    Tax_Accounting_Information = {}
    Pension_Fund = {}
    Social_Insurance = {}
    Authorized_Capital = {}
    Kind_Of_Activity = []
    i = 0
    for index, row in df[1].iterrows():
        if i > 1:
            try:
                if 'ГРН и дата внесения в ЕГРЮЛ' in row[1] and i > 8 and i < 16:
                    continue
                if 'Способ образования' in row[1]:
                    continue
                if 'Дата присвоения ОГРН' in row[1]:
                    continue
                if 'Регистрационный номер, присвоенный до 1' in row[1]:
                    continue
                if 'Дата регистрации до 1 июля 2002 года' in row[1]:
                    continue
                if 'Наименование органа,\rзарегистрировавшего юридическое лицо до\r1 июля 2002 года' in row[1]:
                    continue
                if 'регистрирующ' in row[1]:
                    continue
                dict[row[1].strip()] = row[2]
            except:
                pass
        i += 1
    for index, row in df[2].iterrows():
        try:
            if 'ИНН' in row[1]:
                if row[1] in Tax_Accounting_Information:
                    person[row[1]] = row[2]
                else:
                    Tax_Accounting_Information[row[1]] = row[2]
            if 'КПП' in row[1]:
                Tax_Accounting_Information[row[1]] = row[2]
            if 'Регистрационный номер' in row[1]:
                if row[1] in Pension_Fund:
                    Social_Insurance[row[1]] = row[2]
                else:
                    Pension_Fund[row[1]] = row[2]
            if 'Наименование территориального' in row[1]:
                Pension_Fund[row[1]] = row[2]
            if 'Наименование исполнительного' in row[1]:
                Social_Insurance[row[1]] = row[2]
            if 'Вид' in row[1]:
                Authorized_Capital[row[1]] = row[2]
            if 'Размер' in row[1]:
                Authorized_Capital[row[1]] = row[2]
            if 'Фамилия' in row[1]:
                person[row[1]] = row[2]
            if 'Отчество' in row[1]:
                person[row[1]] = row[2]
            if 'Имя' in row[1]:
                person[row[1]] = row[2]
            if 'Должность' in row[1]:
                person[row[1]] = row[2]
        except:
            pass

    print(dict)
    print(person, Tax_Accounting_Information, Pension_Fund, Social_Insurance, Authorized_Capital)

    i = 3
    j = 0
    while True:
        df = read_pdf(path, multiple_tables=True, encoding='utf-8', spreadsheet=True, pages=str(i))
        for index, row in df[0].iterrows():
            try:
                if 'Код и наименование вида деятельности' in row[1]:
                    Kind_Of_Activity.append(row[2])
                    j += 1
            except:
                pass
        if j == 0:
            break
        else:
            j = 0
            i += 1

        print(Kind_Of_Activity)

tokenOld = parse_nalog(7021004633)
tokenBig = parse_nalog_second_step(7021004633, tokenOld)
parse_nalog_third(tokenBig)
parse_pdf()