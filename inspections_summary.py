import csv
import json
import codecs
import datetime
from datetime import date
from dateutil.tz import gettz
import urllib.request
url = "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4390/%EF%BC%B0%EF%BC%A3%EF%BC%B2%E6%A4%9C%E6%9F%BB%E4%BB%B6%E6%95%B0.csv"
savename = "inspections_summary.csv"
urllib.request.urlretrieve(url, savename)
dt_now = datetime.datetime.now(gettz('Asia/Tokyo'))
da = "{}\/{}\/{} {}:{}".format(dt_now.year, dt_now.month,
                               dt_now.day, dt_now.hour, dt_now.minute)
with open("inspections_summary.csv", encoding="shift_jis") as f:
    reader = csv.DictReader(f, delimiter=",", quotechar='"')
    with open('inspections_summary.json', 'w', encoding="utf-8") as f:
        reader_list = list(reader)
        f.write("{")
        f.write("\n")
        f.write(" \"date\": \"{}\",".format(da))
        f.write("\n")
        f.write(" \"data\": {")
        f.write("\n")
        f.write(" \"県内\": [")
        f.write("\n")
        a = 0
        while a < len(reader_list):
            t = reader_list[a]
            dys = int(t["ＰＣＲ検査件数"])
            if a == len(reader_list) - 1:
                f.write("{}".format(dys))
            else:
                f.write("{},".format(dys))
            f.write("\n")
            a += 1
        f.write("]")
        f.write("\n")
        f.write("},")
        f.write("\n")
        f.write("\"labels\":[")
        f.write("\n")
        a = 0
        while a < len(reader_list):
            t = reader_list[a]
            dys = list(t["検査日"].split("/"))
            if a == len(reader_list) - 1:
                f.write("\"{}\/{}\"".format(dys[1], dys[2]))
            else:
                f.write("\"{}\/{}\",".format(dys[1], dys[2]))
            f.write("\n")
            a += 1
        f.write("]")
        f.write("\n")
        f.write("}")
