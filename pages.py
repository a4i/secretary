import tomllib
import httpx
from bs4 import BeautifulSoup

from utils import erreur_fatale, send_mail

with open("pages.toml", "rb") as f:
    data = tomllib.load(f)

for site in list(data.keys()):

    params = data[site]
    attrs = data[site]['attrs'] if data[site]['attrs'] else True
    tag = data[site]['tag'] if data[site]['tag'] else True
    attr = data[site]['attr']

    try:
        old = open(f"/tmp/secretary_{site}.txt", "r").read()
    except FileNotFoundError:
        old = ""

    try:
        page = httpx.get(params['url'])
    except (httpx.ConnectError, httpx.HTTPError) as e:
        page = None
        erreur_fatale(1, "Erreur HTTP sur " + params['url'], e)

    soup = BeautifulSoup(page.text, 'html.parser')

    result = soup.find(tag, attrs=attrs)
    if attr and result.get(attr):
        result = result[attr]
    else:
        result = str(result)

    if result != old:
        message = site.upper() + "\n\n"
        if old == "":
            message += "First statement: " + result
        else:
            message += f"New statement: {result}\nOld statement: {old}"
        send_mail(message)
        f = open(f"/tmp/secretary_{site}.txt", "w")
        f.write(result)
        f.close()