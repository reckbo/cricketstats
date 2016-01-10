import requests
import urllib2
from bs4 import BeautifulSoup

url =
response = requests.get(url)
try:
    html = response.read()
except Exception:
    raise
else:
    my_parse(html)
finally:
    try:
        response.close()
    except (UnboundLocalError, NameError):
        raise UnboundLocalError

def my_parse(html):
    soup = BeautifulSoup(html)
    table2 = soup.find_all('table')[1]
    for tr in table2.find_all('tr')[2:]:
        tds = tr.find_all('td')
        url = tds[8].a.get('href')
        records.append([elem.text.encode('utf-8') for elem in tds])
        # perhaps you want to update one of the elements of this last
        # record with the found url now?

# It's more efficient to write only once
with open('listing.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(records)
