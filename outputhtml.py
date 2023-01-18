import datetime
import yfinance as yf
import mplfinance as mf
import os
import datetime

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


# 直近四四半期の eps を出力
def draw_eps(data, out_img):
    qis = data.quarterly_income_stmt
    delited_eps = qis.loc['Diluted EPS']
    years = ([str(k).split(" ")[0] for k in list(delited_eps.keys())])
    plt.bar(years, delited_eps.to_list(), color='b', label = 'delited eps', width = 0.3)
    plt.legend(loc=3)
    plt.savefig(out_img)
    

# 直近四四半期の 売上と収益 を出力
def draw_income_and_revenue(data, out_img):
    qis = data.quarterly_income_stmt
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
#   - revenue_and_incomes_img
#   - eps_img
#   - chart_img
#   - output.html
#
# output.html を見ると、チャートと財務状況が一覧で見られる
def out_html(tickers, dirname):
    revenue_and_incomes_img_dir = dirname + "/" + "revenue_and_incomes"
    eps_img_dir = dirname + "/" + "eps_img"
    char_img_dir = dirname + "/" + "char_img"
    os.makedirs(revenue_and_incomes_img_dir)
    os.makedirs(eps_img_dir)
    os.makedirs(char_img_dir)
    
    for ticker in tickers:
        data = yf.Ticker(ticker)
        draw_eps(data, eps_img_dir + "/" + ticker + ".jpg")
        draw_income_and_revenue(data, revenue_and_incomes_img_dir + "/" + ticker + ".jpg")
        draw_chart(ticker, char_img_dir + "/" + ticker + ".jpg")
