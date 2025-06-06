"""
https://disclosure2.edinet-fsa.go.jp/weee0010.aspx
の EDINET コードリストの CSV を標準入力で取り、有効な証券コードを返す。
証券コードをリストアップする際、yahoo finance で読み取れるように、末尾に東証ならT、福証ならF、札証ならSをつける。
名証は現状未実装なので、東証と同様に T を末尾につけている。
"""


import sys
import io
import requests
from bs4 import BeautifulSoup

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='cp932')

# 福証の単独上場企業の証券コードを読み込み
def load_fukusho():
    return load_jpubb("https://www.jpubb.com/list/list.php?listed=1&se=huk&tand=true&page=")

def load_meisyo():
    # jpubb で名証単独が取れないので空
    return []

def load_sassyo():
    return load_jpubb("https://www.jpubb.com/list/list.php?listed=1&se=sa&tand=true&page=")

def load_jpubb(url_base):
    results = []
    i = 0
    while True:
        url = url_base + str(i)
        data = requests.get(url)
        html = data.text
        soup = BeautifulSoup(html, 'html.parser')
        cur_codes = []
        for codeclass in soup.find(class_="corpTable").find_all(class_="code"):
            code = int(codeclass.find("a").text)
            cur_codes.append(code)
        # 要素が全く取れなかったか、前と同じ要素だった場合に終了
        if len(cur_codes) == 0 or (not (len(results) == 0) and cur_codes[-1] == results[-1]):
            break
        results += cur_codes
        i += 1
    return results
    
    

def main():
    # 最初の２行はデータ本体ではないので飛ばす
    skip = 0
    for l in sys.stdin:
        skip += 1
        if skip == 2:
            break
    
    # データ本体の読み込み & 証券コードのリストアップ
    codes = []
    for l in sys.stdin:
        number = (l.split(",")[-2])
        if number != "\"\"":
            codes.append(int(number[1:len(number)-2]))
    

    dic = {}
    for code in load_fukusho():
        dic[code] = 'F'
    for code in load_sassyo():
        dic[code] = 'S'
    # 名証は yahoo finance が対応していないのもあり .T 扱いにしておく
    # スクリーニングの時に yahoo finance api がエラーを返すためにスクリーニング結果から弾かれる

    for code in codes:
        if code in dic:
            print (str(code) + "." + dic[code])
        else:
            print (str(code) + ".T")

main()

