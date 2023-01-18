"""
edinet_to_number.py の出力を numbers.txt から読み込み、スクリーニング関数の条件を満たす証券コードを out.txt に出力する。
"""

import sys
import datetime
import yfinance as yf
import minetrend
import mplfinance as mf

import outputhtml

import matplotlib.pyplot as plt

# ticker を渡して、yfinance.download を実行し、結果を返す
def get_stock_info(num):
    # TODO: 東証以外にも対応したい
    num_str = str(num) + ".T"
    # TODO: 株式分割の影響も考慮して計算できるようにしたい
    # 無理なら株式分割が１年以内にある場合はなにか print したほうがいいかもしれない
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
    
#main()

output_dir = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
outputhtml.out_html(["9984.T"], output_dir)

#draw_chart(7203, "")
#outputhtml.draw_finance("9984.T", "")
