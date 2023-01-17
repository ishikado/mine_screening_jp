"""
edinet_to_number.py の出力を numbers.txt から読み込み、スクリーニング関数の条件を満たす証券コードを out.txt に出力する。
"""

import sys
import datetime
import yfinance as yf
import minetrend

# ticker を渡して、yfinance.download を実行し、結果を返す
def get_stock_info(num):
    num_str = str(num) + ".T"
    data = yf.download(num_str, period='365d', interval = "1d")
    return data

# input_file_name から ticker を改行で区切った入力を受け取り、ticker を key、yfinance.download の結果を value とした dict を返す
def get_stock_infos(input_file_name):
    result_dict = {}
    with open(input_file_name, mode='r') as in_f:
        for num in in_f:
            num = int(num)
            data = get_stock_info(num)
            if not data.empty:
                result_dict[num] = data
    return result_dict

def main():
    output_file_name = "out.txt"
    input_file_name = "numbers.txt"

    slist = get_stock_infos(input_file_name)
    stock_infos = get_stock_infos(input_file_name)

    print ("screening...")
    results = minetrend.screening(stock_infos)
    with open(output_file_name, mode='w') as out_f:
        for num in results:
            print (num, file=out_f)
    print ("done, total_stock = " + str(len(results)))
    
main()
