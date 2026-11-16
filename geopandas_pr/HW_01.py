import pandas as pd
import numpy as np
import requests

inns = pd.read_excel("Реестр_изменённый.xlsx")
inns = inns[inns['Дата исключения из реестра'].isna()]['ИНН']

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://bo.nalog.gov.ru/",
    "Origin": "https://bo.nalog.gov.ru"
})

dataset = []

for inn in inns[0:100000]:
    url = f"https://bo.nalog.gov.ru/advanced-search/organizations/search?query={inn}&page=0"
    response = session.get(url, timeout=10)
    res = response.json()

    if not res.get("content"):
        continue

    company = res["content"][0]

    url_adr = f"https://bo.nalog.gov.ru/nbo/organizations/{company.get('id')}/bfo/"
    response_adr = session.get(url_adr)

    adr_data = response_adr.json()
    adr = adr_data[len(adr_data) - 1]["organizationInfo"]

    if adr is None:
        continue

    company_info = {
        'org_id': company.get('id'),
        'inn': company.get('inn')[8:18],
        'shortName': company.get('shortName'),
        'address': adr.get('address')
    }

    god = []
    for i in range(len(adr_data)):

        if not adr_data[i]['typeCorrections'][0]['correction'].get("financialResult"):
            continue

        fr = adr_data[i]['typeCorrections'][0]['correction']['financialResult']

        cur_val_2300 = fr.get('current2300') or 0
        pre_val_2300 = fr.get('previous2300') or 0
        cur_val_2500 = fr.get('current2500') or 0
        pre_val_2500 = fr.get('previous2500') or 0

        content = {
            'year': adr_data[i]['period'],
            'ubita': cur_val_2300 - pre_val_2300,
            'profit': cur_val_2500 - pre_val_2500
        }
        god.append(content)

    god.sort(key=lambda x: int(x['year']))

    for i in range(len(god)):
        company_info[f"{god[i]['year']} ubita"] = god[i]['ubita']
        company_info[f"{god[i]['year']} profit"] = god[i]['profit']

    dataset.append(company_info)

df = pd.DataFrame(dataset)
df.to_excel("final_dataset.xlsx", index=False)