"""
edinet_to_number.py の出力を標準入力から読み込み、スクリーニング関数の条件を満たす証券コードを出力する。
"""

import sys
import datetime
import yfinance as yf

# data がスクリーニングの条件を満たしているか確認
def is_satisfied(data):
    #    print (datetime.datetime.fromtimestamp(d/1000.0))

    # 現在の値段を取り出し
    for i, r in data.tail(1).iterrows():
        price = float(r["Close"])
    high_52w = -1
    low_52w = 10000000
    sma50 = 0
    sma150 = 0
    sma200 = 0

    # 52w(365d)高値
    for i, r in data.iterrows():
        high_52w = max(high_52w, float(r["High"]))
    # 52w(365d)安値
    for i, r in data.iterrows():
        low_52w = min(low_52w, float(r["Low"]))

    # sma50
    for i, r in data.tail(50).iterrows():
        sma50 += float(r["Close"])
    sma50 /= 50

    # sma150
    for i, r in data.tail(150).iterrows():
        sma150 += float(r["Close"])
    sma150 /= 150

    # sma200
    for i, r in data.tail(200).iterrows():
        sma200 += float(r["Close"])
    sma200 /= 200

    #print (price, high_52w, low_52w, sma50, sma150, sma200)

    if not (price >= 500):
        return False

    if not (price >= sma50 and sma50 >= sma150 and sma150 >= sma200):
        return False

    if not(low_52w * 1.25 <= price):
        return False

    if not(high_52w * 0.75 <= price):
        return False

    # TODO: avg200 が１ヶ月上昇トレンドにあることをチェックする
    

    return True

def get_stock_info(num):
    num_str = str(num) + ".T"
    data = yf.download(num_str, period='365d', interval = "1d")
    return data

def main():
    with open("out2.txt", mode='w') as f:
        for num in sys.stdin:
            num = int(num)
            data = get_stock_info(num)
            if not data.empty and is_satisfied(data):
                print (num, file=f)
            else:
                pass
    print ("done")
    
main()
