import datetime
import yfinance as yf
import mplfinance as mf
import os
import datetime

from jinja2 import Template, Environment, FileSystemLoader

import matplotlib.pyplot as plt

# 直近半年のチャートを出力
def draw_chart(num, out_img):
    # yfinance.download の結果から、チャートを画像に出力する
    # TODO: スクリーニングの時点でこの結果はダウンロード済みなので、受け取るようにしたい
    data = yf.download(num, period='365d', interval = "1d")
    today = datetime.datetime.now()
    before6month = today - datetime.timedelta(days=182)
    start = today.strftime("%Y-%m-%d")
    end = before6month.strftime("%Y-%m-%d")
    mf.plot(data,style='yahoo',type='candle',title=str(num),volume=True, xlim=(start, end), savefig = out_img)


# 直近四年の eps を出力
def draw_eps(data, out_img):
    qis = data.income_stmt
    delited_eps = qis.loc['Diluted EPS']
    years = ([str(k).split(" ")[0] for k in list(delited_eps.keys())])
    plt.bar(years, delited_eps.to_list(), color='b', label = 'delited eps', width = 0.3)
    plt.legend(loc=3)
    plt.savefig(out_img)
    

# 直近四年の 売上と収益 を出力
def draw_income_and_revenue(data, out_img):
    qis = data.income_stmt
    total_revenue = qis.loc['Total Revenue']
    operating_income = qis.loc['Operating Income']

    years = ([str(k).split(" ")[0] for k in list(total_revenue.keys())])

    # print total revenue for past four years.
    #for k in total_revenue.keys():
    #    print (total_revenue[k])

    x1 = [1, 2, 3, 4]
    x2 = [1.3, 2.3, 3.3, 4.3]
     
    plt.bar(x1, total_revenue.to_list(), color='b', label = 'total revenue', width = 0.3)
    plt.bar(x2, operating_income.to_list(), color='g', label = 'operating income', width = 0.3)
    plt.legend(loc=2)
    plt.xticks([1.15, 2.15, 3.15, 4.15], years)
    plt.savefig(out_img)


# dirname 以下に以下の構成でファイルを配置する
#
# - ${dirname}/
#   - tickers
#      - ${ticker}
#         - eps.jpg
#         - income.jpg
#         - chart.jpg
#   - output.html
#
# output.html を見ると、チャートと財務状況が一覧で見られる
def out_html(tickers, dirname):
    tickers_dir = dirname + "/" + "tickers"
    os.makedirs(tickers_dir)
    
    items = []
    for ticker in tickers:
        data = yf.Ticker(ticker)
        ticker_dir = tickers_dir + "/" + ticker
        os.makedirs(ticker_dir)
        draw_eps(data, ticker_dir + "/eps.jpg")
        draw_income_and_revenue(data, ticker_dir + "/income.jpg")
        draw_chart(ticker, ticker_dir + "/chart.jpg")
        img_base_url = "tickers/" + ticker
       
        # TODO: 日本株以外は場合分けしてURLを変える
        ticker_url = "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETsiR001Control&_PageID=WPLETsiR001Idtl30&_DataStoreID=DSWPLETsiR001Control&_ActionID=DefaultAID&s_rkbn=&s_btype=&i_stock_sec=&i_dom_flg=1&i_exchange_code=&i_output_type=2&exchange_code=TKY&stock_sec_code_mul={}&ref_from=1&ref_to=20&wstm4130_sort_id=&wstm4130_sort_kbn=&qr_keyword=&qr_suggest=&qr_sort=".format(ticker.split(".")[0])

        # TODO: class または dict 形式で渡す
        items.append((ticker, ticker_url, img_base_url + "/chart.jpg", img_base_url + "/income.jpg", img_base_url + "/eps.jpg"))

    # output.html を作成する
    # directory の中を読んで、画像の数だけループを作りたい
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tmpl = env.get_template('template/result.html.j2')
    rendered = tmpl.render(items = items)

    with open(dirname + "/" + "output.html", 'w') as f:
        f.write(rendered)
