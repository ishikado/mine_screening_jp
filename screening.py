"""
edinet_to_number.py の出力を numbers.txt から読み込み、スクリーニング関数の条件を満たす証券コードを out.txt に出力する。
"""

import sys
import datetime
import yfinance as yf

# data がスクリーニングの条件を満たしているか確認
def is_satisfied(data):
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

def calc_rs(stock_infos):
    rs_rank = {}
    ls = []
    for num in stock_infos.keys():
        data = stock_infos[num]
        try:
            c = data.iloc[-1]["Close"]
            c63 = data.iloc[-1-63]["Close"]
            c126 = data.iloc[-1-126]["Close"]
            c189 = data.iloc[-1-189]["Close"]
            c252 = data.iloc[-1-252]["Close"]
            # 参考 : https://bullinu.com/2020/07/11/how-to-calc-relativestrength/
            rs_prime = 2 * c / c63  + c / c126 + c / c189 + c / c252
            rs_rank[num] = rs_prime
            ls.append((rs_prime, num))
        except Exception as e:
            print (e)
    ls.sort(reverse=True)
    total = len(ls)
    for i in range(0, total):
        (rs_prime, num) = ls[i]
        rank = int(round(((total - i * 1.0) / total) * 100))
        rs_rank[num] = rank
    return rs_rank

def get_stock_infos(input_file_name):
    result_dict = {}
    with open(input_file_name, mode='r') as in_f:
        for num in in_f:
            num = int(num)
            data = get_stock_info(num)
            if not data.empty:
                result_dict[num] = data
    return result_dict
    

def screening(rs_rank, stock_infos, output_file_name):
    with open(output_file_name, mode='w') as out_f:
        for num in stock_infos.keys():
            # rs_rank 70 以上のみ対象
            if num in rs_rank and rs_rank[num] < 70:
                continue
            data = stock_infos[num]
            if is_satisfied(data):
                print (num, file=out_f)


def main():
    output_file_name = "out.txt"
    input_file_name = "numbers.txt"

    stock_infos = get_stock_infos(input_file_name)

    print ("calc rs...")
    rs_rank = calc_rs(stock_infos)
    print ("done")

    print ("screening...")
    screening(rs_rank, stock_infos, output_file_name)
    print ("done")
    
main()
