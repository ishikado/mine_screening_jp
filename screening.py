"""
edinet_to_number.py の出力を numbers.txt から読み込み、スクリーニング関数の条件を満たす証券コードを out.txt に出力する。
"""

import sys
import datetime
import yfinance as yf
import minetrend
import mplfinance as mf

# ticker を渡して、yfinance.download を実行し、結果を返す
def get_stock_info(num):
    num_str = str(num) + ".T"
    data = yf.download(num_str, period='365d', interval = "1d")
    return data

# input_file_name から ticker を改行で区切った入力を受け取り、ticker を key、yfinance.download の結果を value とした dict を返す
def get_stock_infos():
    result_dict = {}
    for num in sys.stdin:
        num = int(num)
        data = get_stock_info(num)
        if not data.empty:
            result_dict[num] = data
    return result_dict

def main():
    output_file_name = "out.txt"

    stock_infos = get_stock_infos()

    print ("screening...")
    results = minetrend.screening(stock_infos)

    # TODO: 番号だけの text を出力するモードと、ファイナンスの画像やチャートも一緒に出力するモードを実装する

    # ticker を text に出力する
    with open(output_file_name, mode='w') as out_f:
        for num in results:
            print (num, file=out_f)
    print ("done, total_stock = " + str(len(results)))
    
main()


# テスト用実装
def draw_chart(num, out_img):
    # yfinance.download の結果から、チャートを画像に出力する
    data = get_stock_info(num)    
    


    pass
