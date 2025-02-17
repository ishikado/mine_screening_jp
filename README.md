# 概要
ミネルヴィニのスクリーニングテンプレートに則ったスクリーニングを行うツール。

# 使い方
## 日本株
```
$ python3 screening.py -jp < codes.txt

$ ls 日付
out.txt  output.html  tickers
# output.html スクリーニング結果とファイナンス情報とチャートを描画する。
```

## 外国株

```
$ python3 screening.py < tickers.txt
# jp オプションを外す
```

# output.html の例
![キャプチャ](https://user-images.githubusercontent.com/933884/213460590-d639dc90-6289-4f5a-b36f-77889d41c3bb.PNG)


# 動作環境
- python3.7以上

# 必要ライブラリ
- yfinance
- mplfinance
- jinja2
- yahooquery
- urllib3

# ライブラリのインストール
requirements.txt があるのでこれを使ってインストールしてください。
venv 等を使って仮想環境を作ってそこにいれることをおすすめします。
