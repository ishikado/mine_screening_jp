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

    tickers = []

    for f in soup.find_all(class_="mgt10"):
        tbody = f.find("tbody")
        if not tbody == None:
            for a in tbody.find_all("tr"):
                for b in a.find_all(class_="thM alC"):
                    ticker = b.find(class_="fm01").text
                    tickers.append(ticker)
                    #print (ticker)

    # TODO: 普通株式以外の銘柄も取得できるようにする
    for a in soup.find(class_="foo_table md-l-table-01 md-l-utl-mt10").tbody.find_all("tr"):
        l = []
        for b in a.find_all(class_="vaM alC"):
            l.append(b.text)
        ticker, market = l[0], l[1]
        tickers.append(ticker)
    #     print (ticker)
    
    for ticker in tickers:
        print (ticker)


main()
