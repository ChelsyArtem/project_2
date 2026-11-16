import pandas as pd
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

    company_info = {
        'shortName': res["content"][0]['shortName'],
        'address': f"{res["content"][0]["region"]} Область, {res["content"][0]["street"]} ул, д. {res["content"][0]["house"]}",
        'gainsum': res["content"][0]["bfo"]["gainSum"]
    }

    dataset.append(company_info)

df = pd.DataFrame(dataset)
df = df.sort_values(by='gainsum', ascending=False)[0:500]
df.to_excel("map_dataset.xlsx", index=False)