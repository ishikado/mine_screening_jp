"""
edinet_to_number.py の出力を numbers.txt から読み込み、スクリーニング関数の条件を満たす証券コードを out.txt に出力する。
"""

import sys
import datetime
import yfinance as yf
import minetrend
import mplfinance as mf
import argparse
import os

import outputhtml

import matplotlib.pyplot as plt

# ticker を渡して、yfinance.download を実行し、結果を返す
def get_stock_info(num):
    # TODO: 株式分割の影響も考慮して計算できるようにしたい
    # 無理なら株式分割が１年以内にある場合はなにか print したほうがいいかもしれない
    data = yf.download(num, period='365d', interval = "1d")
    return data

# input_file_name から ticker を改行で区切った入力を受け取り、ticker を key、yfinance.download の結果を value とした dict を返す
def get_stock_infos():
    result_dict = {}
    for num in sys.stdin:
        num = num.strip()
        data = get_stock_info(num)
        if not data.empty:
            result_dict[num] = data
    return result_dict

def main():

    parser = argparse.ArgumentParser(description='screening stocks')
    parser.add_argument('-jp', action='store_true')
    args = parser.parse_args()
    is_jp = args.jp

    stock_infos = get_stock_infos()

    print ("screening...")
    results = minetrend.screening(stock_infos, is_jp)

    output_dir = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs(output_dir)
    # ticker を text に出力する
    output_text = output_dir + "/" + "out.txt"
    with open(output_text, mode='w') as out_f:
        for num in results:
            print (num, file=out_f)
    # ticker をファイナンス情報と一緒に html に出力する
    outputhtml.out_html(results, output_dir, is_jp)

    print ("done, total_stock = " + str(len(results)))

    
main()
