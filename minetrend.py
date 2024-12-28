import yfinance as yf

# data がスクリーニングの条件を満たしているか確認
# data は yfinance.download の返り値
def is_satisfied(data, is_jp):
    # 現在の値段を取り出し
    for i, r in data.tail(1).iterrows():
        price = float(r.iloc[0])
        
    high_52w = -1
    low_52w = 10000000
    sma50 = 0
    sma150 = 0
    sma200 = 0

    # 52w(365d)高値
    for i, r in data.iterrows():
        high_52w = max(high_52w, float(r.iloc[1]))
    # 52w(365d)安値
    for i, r in data.iterrows():
        low_52w = min(low_52w, float(r.iloc[2]))

    # sma50
    for i, r in data.tail(50).iterrows():
        sma50 += float(r.iloc[0])
    sma50 /= 50

    # sma150
    for i, r in data.tail(150).iterrows():
        sma150 += float(r.iloc[0])
    sma150 /= 150

    # sma200
    for i, r in data.tail(200).iterrows():
        sma200 += float(r.iloc[0])
    sma200 /= 200

    if is_jp:
        if not (price >= 500):
            return False
    else:
        if not (price >= 10):
            return False
        

    if not (price >= sma50 and sma50 >= sma150 and sma150 >= sma200):
        return False

    if not(low_52w * 1.25 <= price):
        return False

    if not(high_52w * 0.75 <= price):
        return False

    # TODO: avg200 が１ヶ月上昇トレンドにあることをチェックする
    
    return True

def calc_rs(stock_infos):
    rs_rank = {}
    ls = []
    for ticker in stock_infos.keys():
        data = stock_infos[ticker]
        try:
            c = data.iloc[-1]["Close"]
            c63 = data.iloc[-1-63]["Close"]
            c126 = data.iloc[-1-126]["Close"]
            c189 = data.iloc[-1-189]["Close"]
            c252 = data.iloc[-1-252]["Close"]
            # 参考 : https://bullinu.com/2020/07/11/how-to-calc-relativestrength/
            rs_prime = 2 * c / c63  + c / c126 + c / c189 + c / c252
            rs_rank[ticker] = rs_prime
            ls.append((rs_prime, ticker))
        except Exception as e:
            print (e)
    ls.sort(reverse=True)
    total = len(ls)
    for i in range(0, total):
        (rs_prime, ticker) = ls[i]
        rank = int(round(((total - i * 1.0) / total) * 100))
        rs_rank[ticker] = rank
    return rs_rank

# stock_infos は ticker を key、yfinance.download の結果を value とする dict
def screening(stock_infos, is_jp):
    print ("calc rs...")
    rs_rank = calc_rs(stock_infos)
    print ("done")
    results = []
    for ticker in stock_infos.keys():
        # rs_rank 70 以上のみ対象
        if ticker in rs_rank and rs_rank[ticker] < 70:
            continue
        data = stock_infos[ticker]
        if is_satisfied(data, is_jp):
            results.append(ticker)
    return results
