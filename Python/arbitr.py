import requests

def arbitr_get_html():
    url = "http://kad.arbitr.ru/Kad/SearchInstances"

    payload = "{\n\t\"CaseNumbers\": [],\n\t\"Count\": 25,\n\t\"Courts\": [],\n\t\"DateFrom\": null,\n\t\"DateTo\": null,\n\t\"Judges\": [],\n\t\"Page\": 1,\n\t\"Sides\": \n\t\t[\n\t\t\t{\n\t\t\t\t\"Name\": \"7021004633\", \n\t\t\t\t\"Type\": -1, \n\t\t\t\t\"ExactMatch\": false\n\t\t\t\t\n\t\t\t}\n\t\t],\n\t\"WithVKSInstances\": false\n}"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "f1509a00-989f-4ec3-af9f-0a764b33fa98"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)