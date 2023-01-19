import datetime
import yfinance as yf
import mplfinance as mf
import os
import datetime

from jinja2 import Template, Environment, FileSystemLoader

import matplotlib.pyplot as plt

# 直近半年のチャートを出力
def draw_chart(ticker, stock_infos, out_img):
    # yfinance.download の結果から、チャートを画像に出力する
    data = stock_infos[ticker]
    today = datetime.datetime.now()
    before6month = today - datetime.timedelta(days=182)
    start = before6month.strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")
    mf.plot(data,style='yahoo',type='candle',title=str(ticker),volume=True, xlim=(start, end), savefig = out_img)


# 直近四年の eps を出力
def draw_eps(data, out_img):
    diluted_eps_str = 'Diluted EPS'
    qis = data.income_stmt
    # ない場合はグラフを作らない
    if not diluted_eps_str in qis.index:
        return

    delited_eps = qis.loc[diluted_eps_str]
    years = ([str(k).split(" ")[0] for k in list(reversed(list(delited_eps.keys())))])
    plt.bar(years, list(reversed(delited_eps.to_list())), color='b', label = 'delited eps', width = 0.3)
    plt.title(diluted_eps_str)
    plt.savefig(out_img)
    plt.clf()    

def draw_net_income(data, out_img):
    net_income_str = 'Net Income'
    qis = data.income_stmt
    if not net_income_str in qis.index:
        return
    net_income = qis.loc[net_income_str]
    years = ([str(k).split(" ")[0] for k in list(reversed(list(net_income.keys())))])
    plt.bar(years, list(reversed(net_income.to_list())), color='b', label = 'net income', width = 0.3)
    plt.title(net_income_str)
    plt.savefig(out_img)
    plt.clf()    

def draw_revenue(data, out_img):
    total_revenue_str = 'Total Revenue'
    qis = data.income_stmt
    if not total_revenue_str in qis.index:
        return
    total_revenue = qis.loc[total_revenue_str]
    years = ([str(k).split(" ")[0] for k in list(reversed(list(total_revenue.keys())))])
    plt.bar(years, list(reversed(total_revenue.to_list())), color='b', label = 'total revenue', width = 0.3)
    plt.title(total_revenue_str)
    plt.savefig(out_img)
    plt.clf()    

def draw_operating_income(data, out_img):
    operating_income_str = 'Operating Income'
    qis = data.income_stmt
    if not operating_income_str in  qis.index:
        return
    operating_income = qis.loc[operating_income_str]
    years = ([str(k).split(" ")[0] for k in list(reversed(list(operating_income.keys())))])
    plt.bar(years, list(reversed(operating_income.to_list())), color='b', label = 'operating income', width = 0.3)
    plt.title(operating_income_str)
    plt.savefig(out_img)
    plt.clf()    

# output.html を見ると、チャートと財務状況が一覧で見られる
def out_html(tickers, stock_infos, dirname, is_jp):
    tickers_dir = dirname + "/" + "tickers"
    os.makedirs(tickers_dir)
    
    items = []
    for ticker in tickers:
        data = yf.Ticker(ticker)

        # 上場廃止の場合は finance data が取れず empty となるので無視する
        if data.income_stmt.empty:
            continue

        # for debug
        print (ticker)

        ticker_dir = tickers_dir + "/" + ticker
        os.makedirs(ticker_dir)
        draw_eps(data, ticker_dir + "/eps.jpg")
        draw_revenue(data, ticker_dir + "/revenue.jpg")
        draw_operating_income(data, ticker_dir + "/operating_income.jpg")
        draw_net_income(data, ticker_dir + "/net_income.jpg")
        #draw_income_and_revenue(data, ticker_dir + "/income.jpg")
        draw_chart(ticker, stock_infos, ticker_dir + "/chart.jpg")
        img_base_url = "tickers/" + ticker
       
        if is_jp:
            ticker_url = "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETsiR001Control&_PageID=WPLETsiR001Idtl30&_DataStoreID=DSWPLETsiR001Control&_ActionID=DefaultAID&s_rkbn=&s_btype=&i_stock_sec=&i_dom_flg=1&i_exchange_code=&i_output_type=2&exchange_code=TKY&stock_sec_code_mul={}&ref_from=1&ref_to=20&wstm4130_sort_id=&wstm4130_sort_kbn=&qr_keyword=&qr_suggest=&qr_sort=".format(ticker.split(".")[0])
        else:
            ticker_url = "https://finance.yahoo.com/quote/" + ticker

        # TODO: class または dict 形式で渡す
        items.append((ticker, ticker_url, img_base_url + "/chart.jpg", img_base_url + "/revenue.jpg", img_base_url + "/operating_income.jpg", img_base_url + "/net_income.jpg", img_base_url + "/eps.jpg"))

    # output.html を作成する
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tmpl = env.get_template('template/result.html.j2')
    rendered = tmpl.render(items = items)

    with open(dirname + "/" + "output.html", 'w') as f:
        f.write(rendered)
