import requests
from bs4 import BeautifulSoup as bs

def arbitr_get_html():
    url = "http://kad.arbitr.ru/Kad/SearchInstances"

    payload = "{\n\t\"CaseNumbers\": [],\n\t\"Count\": 25,\n\t\"Courts\": [],\n\t\"DateFrom\": null,\n\t\"DateTo\": null,\n\t\"Judges\": [],\n\t\"Page\": 1,\n\t\"Sides\": \n\t\t[\n\t\t\t{\n\t\t\t\t\"Name\": \"7021004633\", \n\t\t\t\t\"Type\": -1, \n\t\t\t\t\"ExactMatch\": false\n\t\t\t\t\n\t\t\t}\n\t\t],\n\t\"WithVKSInstances\": false\n}"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "f1509a00-989f-4ec3-af9f-0a764b33fa98"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    answer = bs(response.text, 'html.parser')
    print(answer)
    return answer

def arbitr_parse(answer):
    url = []
    name_deal = []
    judge = []
    court = []
    plaintiff = {'name': None, 'inn': None, 'address': None, 'index': None}
    respondent = {'name': None, 'inn': None, 'address': None, 'index': None}
    for ans in answer.find_all('tr'):
        print('')
        print(ans.span.text)        #дата заседания
        for div in ans.find_all('a', class_='num_case'):
            print(div.get('href'))                              #ссылка на дело
            #url.append(div.get('href'))
            print(str(ans.a.text).strip())                                #название дела
            #name_deal.append(ans.a.text)
        for div in ans.find_all('td', class_='court'):
            print(div.find(class_='judge').get('title'))        #судья
            #judge.append(div.find(class_='judge').get('title'))
            print(div.find(class_=None).get('title'))           #суд
            #court.append(div.find(class_=None).get('title'))
        for div11 in ans.find_all('td', class_='plaintiff'):
            for div1 in div11.find_all('span', class_='js-rollover b-newRollover'):
                data = str(div1.span.text).strip().split('\r')
                if len(data) == 4:
                    plaintiff['name'] = data[0].strip()
                    plaintiff['index'] = data[1].strip().split(',')[0]
                    plaintiff['address'] = ''.join(data[1].strip().split(',')[1:])
                    plaintiff['inn'] = data[3].strip()
                if len(data) == 2:
                    plaintiff['name'] = data[0].strip()
                    plaintiff['index'] = data[1].strip().split(',')[0]
                    plaintiff['address'] = ''.join(data[1].strip().split(',')[1:])
                print('Истец: ', plaintiff)
        for div11 in ans.find_all('td', class_='respondent'):
            for div1 in div11.find_all('span', class_='js-rollover b-newRollover'):
                data = str(div1.span.text).strip().split('\r')
                if len(data) == 4:
                    respondent['name'] = data[0].strip()
                    respondent['index'] = data[1].strip().split(',')[0]
                    respondent['address'] = ''.join(data[1].strip().split(',')[1:])
                    respondent['inn'] = data[3].strip()
                if len(data) == 2:
                    respondent['name'] = data[0].strip()
                    respondent['index'] = data[1].strip().split(',')[0]
                    respondent['address'] = ''.join(data[1].strip().split(',')[1:])
                print('За Базар Ответчик: ', respondent)

ans = arbitr_get_html()
arbitr_parse(ans)