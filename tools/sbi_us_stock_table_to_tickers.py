# https://search.sbisec.co.jp/v2/popwin/info/stock/pop6040_usequity_list.html から ticker 一覧のリストを作成し、標準出力に出力する

import requests
from bs4 import BeautifulSoup

def main():

    url = "https://search.sbisec.co.jp/v2/popwin/info/stock/pop6040_usequity_list.html"
    data = requests.get(url)
    html = data.text
#    with open("out.txt") as f:
#        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    for a in soup.find(class_="md-l-table-01 md-l-utl-mt10").tbody.find_all("tr"):
        l = []
        for b in a.find_all(class_="vaM alC"):
            l.append(b.text)
        ticker, market = l[0], l[1]
        print (ticker)
    

main()
