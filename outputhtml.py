import datetime
import yfinance as yf
import mplfinance as mf

import matplotlib.pyplot as plt

# テスト用実装
def draw_chart(num, out_img):
    # yfinance.download の結果から、チャートを画像に出力する
    data = get_stock_info(num)    
    # TODO: 現在の日付と、6ヶ月前の日付を入力できるようにする
    chart = mf.plot(data,style='yahoo',type='candle',title=str(num),volume=True, xlim=('2022-07-17', '2023-01-17'))
    # TODO: 画像ファイルに出力する
    pass


# 該当 tick の売上、収益、EPS の変化を図に出力する
# 四年分のものと、四半期４期分のものを出したいが、とりあえず四年分のものを先に出す
def draw_finance(num, out_img):
    data = yf.Ticker(str(num))
    #draw_eps(data, out_img)
    draw_income_and_revenue(data, out_img)

def draw_eps(data, out_img):
    qis = data.quarterly_income_stmt
    delited_eps = qis.loc['Diluted EPS']
    years = ([str(k).split(" ")[0] for k in list(delited_eps.keys())])
    plt.bar(years, delited_eps.to_list(), color='b', label = 'delited eps', width = 0.3)
    plt.legend(loc=3)
    plt.show()
    

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
    #plt.bar(x3, delited_eps.to_list(), color='b', label = 'delited eps', width = 0.3)
    plt.legend(loc=2)
    plt.xticks([1.15, 2.15, 3.15, 4.15], years)
    plt.show()
