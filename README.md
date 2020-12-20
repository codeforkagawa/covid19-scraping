# covid19-scraping
[香川県新型コロナウイルス感染症対策非公式サイト](https://kagawa.stopcovid19.jp/)のデータ自動更新用のスクリプトです。

## 環境
Pythonの最新バージョンでの動作を確認しています。

## 実行
Linux・Mac OSの場合は
``` bash
pip3 install -r requirements.txt
python3 script.py
```

Windowsの場合は

``` bash
pip install -r requirements.txt
python script.py
```

で実行されます。

## データ元について
https://opendata.pref.kagawa.lg.jp/dataset/359.html に掲載されている各種ファイルを取得しています。また、

## 生成されるファイルについて

生成されるファイルはすべて`data`ディレクトリ内に生成されます。

### 生成されるファイルの詳細
```
contacts.json（一般相談件数のファイル）
inspections_summary.json （検査実施のファイル）
querents.json（受診相談件数に関するファイル）
news.json (新型コロナウイルス感染症関連の最新ニュース)
main_summary.json（香川県での感染拡大の状況）
patients_summary.json（感染者数の推移）
patients.json（感染者の詳細情報）
```