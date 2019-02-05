import requests
from bs4 import BeautifulSoup as bs

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

    response = requests.request("POST", url, data=payload, headers=headers)
    answer = bs(response.text, 'html.parser')

    print(answer)

string = {"CaseNumbers": [],"Courts": [],"DateFrom": "null","DateTo": "null","Judges": [],"Page": 1,"Sides": [{"Name": 7021004633,"Type": -1,"ExactMatch": "false"}]}

arbitr_get_html(params=string)
