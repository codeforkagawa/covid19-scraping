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
url = "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4391/%E5%8F%97%E8%A8%BA%E7%9B%B8%E8%AB%87%E4%BB%B6%E6%95%B0.csv"
savename = "querents.csv"
urllib.request.urlretrieve(url, savename)
dt_now = datetime.datetime.now(gettz('Asia/Tokyo'))
da = "{}\/{}\/{} {}:{}".format(dt_now.year, dt_now.month,
                               dt_now.day, dt_now.hour, dt_now.minute)
with open("querents.csv", encoding="shift_jis") as f:
    reader = csv.DictReader(f, delimiter=",", quotechar='"')
    with open('querents.json', 'w', encoding="utf-8") as f:
        f.write("{")
        f.write("\n")
        f.write(" \"date\": \"{}\",".format(da))
        f.write("\n")
        f.write(" \"data\": [")
        f.write("\n")
        reader_list = list(reader)
        i = 0
        while i < len(reader_list):
            f.write("{")
            f.write("\n")
            t = reader_list[i]
            n = 0
            d = list(t["相談日"].split("/"))
            if len(d[1]) == 1:
                d[1] = "0" + d[1]
            if len(d[2]) == 1:
                d[2] = "0" + d[2]
            f.write(
                "\"日付\": \"{}-{}-{}T03:00:00.000Z\",".format(d[0], d[1], d[2]))
            f.write("\n")
            f.write("\"小計\":{},".format(t["「帰国者・接触者相談センター」受診相談件数"]))
            f.write("\n")
            f.write("\"short_date\":\"" + d[1] + "\/" + d[2] + "\",")
            f.write("\n")
            dys = ["日", "月", "火", "水", "木", "金", "土"]
            dy = date(int(d[0]), int(d[1]), int(d[2])).weekday()
            if dy == 6:
                dy = 0
            else:
                dy += 1
            f.write("\"w\":{},".format(i + 1))
            f.write("\n")
            f.write("\"曜日\":{},".format(43871 + i))
            f.write("\n")
            f.write("\"date\":\"{}-{}-{}\"".format(d[0], d[1], d[2]))
            f.write("\n")
            if i == len(reader_list) - 1:
                f.write("}")
            else:
                f.write("},")
            f.write("\n")
            i += 1
        f.write("   ]")
        f.write("\n")
        f.write("}")
url = "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4392/%E4%B8%80%E8%88%AC%E7%9B%B8%E8%AB%87%E4%BB%B6%E6%95%B0.csv"
savename = "contacts.csv"
urllib.request.urlretrieve(url, savename)
dt_now = datetime.datetime.now(gettz('Asia/Tokyo'))
da = "{}\/{}\/{} {}:{}".format(dt_now.year, dt_now.month,
                               dt_now.day, dt_now.hour, dt_now.minute)
with open("contacts.csv", encoding="shift_jis") as f:
    reader = csv.DictReader(f, delimiter=",", quotechar='"')
    with open('contacts.json', 'w', encoding="utf-8") as f:
        f.write("{")
        f.write("\n")
        f.write(" \"date\": \"{}\",".format(da))
        f.write("\n")
        f.write(" \"data\": [")
        f.write("\n")
        reader_list = list(reader)
        i = 0
        while i < len(reader_list):
            f.write("{")
            f.write("\n")
            t = reader_list[i]
            n = 0
            types = [
                "県民",
                "医療機関",
                "行政機関",
                "企業",
                "観光・旅館",
                "その他"
            ]
            for tp in types:
                n += int(t["「帰国者・接触者相談センター」一般相談件数（" + tp + "）"])
            d = list(t["相談日"].split("/"))
            if len(d[1]) == 1:
                d[1] = "0" + d[1]
            if len(d[2]) == 1:
                d[2] = "0" + d[2]
            f.write(
                "\"日付\": \"{}-{}-{}T03:00:00.000Z\",".format(d[0], d[1], d[2]))
            f.write("\n")
            f.write("\"小計\":{},".format(n))
            f.write("\n")
            f.write("\"short_date\":\"" + d[1] + "\/" + d[2] + "\",")
            f.write("\n")
            dys = ["日", "月", "火", "水", "木", "金", "土"]
            dy = date(int(d[0]), int(d[1]), int(d[2])).weekday()
            if dy == 6:
                dy = 0
            else:
                dy += 1
            f.write("\"w\":{},".format(dy))
            f.write("\n")
            f.write("\"曜日\":\"{}\",".format(dys[dy]))
            f.write("\n")
            f.write("\"date\":\"{}-{}-{}\"".format(d[0], d[1], d[2]))
            f.write("\n")
            if i == len(reader_list) - 1:
                f.write("}")
            else:
                f.write("},")
            f.write("\n")
            i += 1
        f.write("   ]")
        f.write("\n")
        f.write("}")
