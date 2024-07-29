import datetime
import yfinance as yf
import mplfinance as mf
import os
import datetime
import yahooquery
import time
import pandas as pd


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
    draw_finance_common('DilutedEPS', data, out_img, True)

def draw_net_income(data, out_img):
    draw_finance_common('NetIncome', data, out_img, True)

def draw_revenue(data, out_img):
    draw_finance_common('TotalRevenue', data, out_img, True)

def draw_operating_income(data, out_img):
    draw_finance_common('OperatingIncome', data, out_img, True)

def draw_finance_common(stmt_field_name, data, out_img, use_ttm):
    income_stmt = data.income_statement()

    # income_stmt から最後以外のTTM行を削除する
    last_row = income_stmt[-1:]
    income_stmt_without_last = income_stmt[0:len(income_stmt)-1]
    income_stmt = pd.concat([income_stmt_without_last[income_stmt_without_last["periodType"] != "TTM"], last_row])

    if not stmt_field_name in income_stmt.columns:
        # TODO: ticker name も出したい
        print ("failed to draw " + stmt_field_name)
        return

    stmt_field_value = income_stmt[stmt_field_name]
    years = [datetime.datetime.fromtimestamp(k / 1000 / 1000 / 1000).strftime("%Y-%m-%d") for k in income_stmt["asOfDate"].values.tolist()]
    if income_stmt["periodType"].to_list()[-1] == "TTM":
        years[-1] = "TTM"

    drawed = stmt_field_value.to_list()

    plt.bar(years, drawed, color='b', label = stmt_field_name, width = 0.3)
    plt.title(stmt_field_name)
    plt.savefig(out_img)
    plt.clf()    

# output.html を見ると、チャートと財務状況が一覧で見られる
def out_html(tickers, stock_infos, dirname, is_jp):
    tickers_dir = dirname + "/" + "tickers"
    os.makedirs(tickers_dir)
    
    items = []
    for ticker in tickers:
        # query を送りすぎるとアクセス制限をくらうようなので、sleep して間隔をあける
        # 制限をくらいすぎる場合、sleep 間隔を考えたほうがいいかもしれない
        time.sleep(1)

        data = yahooquery.Ticker(ticker)

        # 一部データは finance data が取れず dataframe 以外の値となるので無視する
        income_stmt = data.income_statement()
        if type(income_stmt) is pd.DataFrame:
            print (ticker +  " data is not found, income_stmt is not Dataframe, type is " + type(income_stmt))
            continue

        # for debug
        print (ticker)

        ticker_dir = tickers_dir + "/" + ticker
        os.makedirs(ticker_dir)

        draw_eps(data, ticker_dir + "/eps.jpg")
        draw_revenue(data, ticker_dir + "/revenue.jpg")
        draw_operating_income(data, ticker_dir + "/operating_income.jpg")
        draw_net_income(data, ticker_dir + "/net_income.jpg")
        # TODO: 週足も出せるようにしたい
        draw_chart(ticker, stock_infos, ticker_dir + "/chart.jpg")
        img_base_url = "tickers/" + ticker
       
        if is_jp:
            ticker_url = "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETsiR001Control&_PageID=WPLETsiR001Idtl30&_DataStoreID=DSWPLETsiR001Control&_ActionID=DefaultAID&s_rkbn=&s_btype=&i_stock_sec=&i_dom_flg=1&i_exchange_code=&i_output_type=2&exchange_code=TKY&stock_sec_code_mul={}&ref_from=1&ref_to=20&wstm4130_sort_id=&wstm4130_sort_kbn=&qr_keyword=&qr_suggest=&qr_sort=".format(ticker.split(".")[0])
        else:
            ticker_url = "https://finance.yahoo.com/quote/" + ticker

        items.append({"ticker" : ticker, 
                      "ticker_url" : ticker_url,
                      "chart_path" : img_base_url + "/chart.jpg",
                      "revenue_path" : img_base_url + "/revenue.jpg",
                      "operating_income_path" : img_base_url + "/operating_income.jpg",
                      "net_income_path" : img_base_url + "/net_income.jpg",
                      "eps_path" : img_base_url + "/eps.jpg"})

    # output.html を作成する
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tmpl = env.get_template('template/result.html.j2')
    rendered = tmpl.render(items = items)

    with open(dirname + "/" + "output.html", 'w') as f:
        f.write(rendered)
