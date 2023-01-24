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
def get_stock_info(ticker):
    # TODO: 株式分割の影響も考慮して計算できるようにしたい
    # 無理なら株式分割が１年以内にある場合はなにか print したほうがいいかもしれない
    data = yf.download(ticker, period='365d', interval = "1d", threads = False)
    return data

# input_file_name から ticker を改行で区切った入力を受け取り、ticker を key、yfinance.download の結果を value とした dict を返す
def get_stock_infos():
    result_dict = {}
    for ticker in sys.stdin:
        ticker = ticker.strip()
        data = get_stock_info(ticker)
        if not data.empty:
            result_dict[ticker] = data
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
        for ticker in results:
            print (ticker, file=out_f)
    # ticker をファイナンス情報と一緒に html に出力する
    # NOTE: スクリーニング結果を入力に取り、out_html を出力するモードがあってもいいかもしない、もしくはその機能はツールを分離するなど
    #       スクリーニングが実行できても out_html の出力部分で失敗するケースが時々見られるため
    #       html_out だけ debug したいケースも多々あるので、そんな感じにしたい
    outputhtml.out_html(results, stock_infos, output_dir, is_jp)

    # 企業の情報からsector及びindustryごとに何件screeningされたかを出力する
    # NOTE: 標準出力ではなくファイルや、output_html の結果に乗せて、後で見られるようにしたほうがいいかもしれない
    sectors = {}
    industries = {}
    for ticker in results:
        tinfo = yf.Ticker(ticker)
        if "sector" in tinfo.info:
            s = tinfo.info["sector"]
            if not s in sectors:
                sectors[s] = 0
            sectors[s] += 1
        if "industry" in tinfo.info:
            i = tinfo.info["industry"]
            if not i in industries:
                industries[i] = 0
            industries[i] += 1

    output_sectors = output_dir + "/" + "sectors.txt"
    with open(output_sectors, mode='w') as out_f:
        print ("industries", file=out_f)
        industries = sorted(industries.items(),key=lambda x:-x[1])
        industries = dict((x, y) for x, y in industries)
        print (industries, file=out_f)
        
        print ("sectors", file=out_f)
        sectors = sorted(sectors.items(),key=lambda x:-x[1])
        sectors = dict((x, y) for x, y in sectors)
        print (sectors, file=out_f)
        

    print ("done, total_stock = " + str(len(results)))

   
main()
