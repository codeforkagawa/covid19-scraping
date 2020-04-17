# covid19-scraping
香川県のデータを取得自動更新
## 環境
Pythonの最新の実行環境（4月18日現在は3.8.2）を必要とします。
## 実行
Linux・OS Xの場合は

``` 
python3 script.py
```

Windowsの場合は

```
python script.py
```
で実行されます。

## データ元について
https://opendata.pref.kagawa.lg.jp/dataset/359.html に掲載されている各種ファイルを取得しています。
## 生成されるファイルについて
```
contacts.json（一般相談件数のファイル）
contacts.csv （県サイトからスクレイピングしたファイル）
inspections_summary.json （検査実施のファイル）
inspections_summary.csv（県サイトよりスクレイピングしたファイル）
querents.json（受診相談件数に関するファイル）
querents.csv（県サイトより取得したファイル）
```
