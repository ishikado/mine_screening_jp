"""
https://disclosure.edinet-fsa.go.jp/E01EW/BLMainController.jsp?uji.verb=W1E62071InitDisplay&uji.bean=ee.bean.W1E62071.EEW1E62071Bean&TID=W1E62071&PID=currentPage&SESSIONKEY=1662729632391&kbn=2&ken=58&res=58&idx=0&start=1&end=58&spf1=1&spf2=1&spf5=1&psr=1&pid=0&row=100&str=&flg=&lgKbn=2&pkbn=0&skbn=1&dskb=&askb=&dflg=0&iflg=0&preId=1
の EDINET コードリストの CSV を標準入力で取り、有効な証券コードを返す。
"""


import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='cp932')

# 最初の２行はデータ本体ではないので飛ばす
skip = 0
for l in sys.stdin:
    skip += 1
    if skip == 2:
        break

# データ本体の読み込み & 証券コードのリストアップ
for l in sys.stdin:
    number = (l.split(",")[-2])
    if number != "\"\"":
        print (number[1:len(number)-2])
