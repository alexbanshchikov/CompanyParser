import requests
from bs4 import BeautifulSoup as bs

import time

def arbitr_get_html(params, count=25, vks="false"):
    url = "http://kad.arbitr.ru/Kad/SearchInstances"

    payload = "{" \
                  "CaseNumbers: " + str(params["CaseNumbers"]) + "," \
                  "Count: " + str(count) + "," \
                  "Courts: " + str(params["Courts"]) + "," \
                  "DateFrom: " + str(params["DateFrom"]) + "," \
                  "DateTo: " + str(params["DateTo"]) + "," \
                  "Judges: " + str(params["Judges"]) + "," \
                  "Page: " + str(params["Page"]) + "," \
                  "Sides: " + str(params["Sides"]) + ","\
                  "WithVKSInstances: " + str(vks) + "" \
              "}"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
        }
    start_time = time.time()
    response = requests.request("POST", url, data=payload, headers=headers)
    answer = bs(response.text, 'html.parser')
    print("--- %s seconds ---" % (time.time() - start_time))
    return answer

def arbitr_parse(answer):
    deal = {'date': None, 'URL': None, 'judge': None, 'court': None, 'name': None, 'plaintiff': None, 'respondent': None}
    plaintiff = {'name': None, 'inn': None, 'address': None, 'index': None}
    respondent = {'name': None, 'inn': None, 'address': None, 'index': None}
    for ans in answer.find_all('tr'):
        print('')
        deal['date'] = ans.span.text
        for div in ans.find_all('a', class_='num_case'):
            deal['URL'] = div.get('href')
            deal['name'] = str(ans.a.text).strip()
        for div in ans.find_all('td', class_='court'):
            deal['judge'] = div.find(class_='judge').get('title')
            deal['court'] = div.find(class_=None).get('title')
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
                deal['plaintiff'] = plaintiff
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
                deal['respondent'] = respondent
                print(deal)


queryString = {"CaseNumbers": [], "Courts": [], "DateFrom": "null", "DateTo": "null", "Judges": [], "Page": 1, "Sides":
    [{"Name": 7021004633, "Type": -1, "ExactMatch": "false"}]}

ans = arbitr_get_html(queryString)
arbitr_parse(ans)
