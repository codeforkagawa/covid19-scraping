import csv
import json
import codecs
import re
from lxml import html
from datetime import datetime, timedelta
import urllib.request
import requests
import feedparser


def generateSummary(updated_at):
    inspectionTemplate = {
        "date": updated_at,
        "data": {},
        "labels": []
    }
    patientsTemplate = {
        "date": updated_at,
        "data": []
    }
    url = "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4390/%EF%BC%B0%EF%BC%A3%EF%BC%B2%E6%A4%9C%E6%9F%BB%E4%BB%B6%E6%95%B0.csv"
    res = urllib.request.urlopen(url)
    reader = csv.DictReader(codecs.iterdecode(
        res, 'shift_jis'), delimiter=",", quotechar='"')
    inspectionTemplate["data"] = {
        "県内": [],
    }
    for row in reader:
        inspectionTemplate["data"]["県内"].append(int(row["ＰＣＲ検査件数"]))
        inspectionTemplate["labels"].append(datetime.strptime(
            row["検査日"], "%Y/%m/%d").strftime("%-m/%-d"))
        patientsTemplate["data"].append({
            "日付": datetime.strptime(row["検査日"], "%Y/%m/%d").strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "小計": int(row["結果（陽性）"])
        })
    filename = 'data/inspections_summary.json'
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(inspectionTemplate, f, indent=4, ensure_ascii=False)
    filename = 'data/patients_summary.json'
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(patientsTemplate, f, indent=4, ensure_ascii=False)


def generateQuerents(updated_at):
    template = {
        "date": updated_at,
        "data": []
    }
    url = "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4391/%E5%8F%97%E8%A8%BA%E7%9B%B8%E8%AB%87%E4%BB%B6%E6%95%B0.csv"
    res = urllib.request.urlopen(url)
    reader = csv.DictReader(codecs.iterdecode(
        res, 'shift_jis'), delimiter=",", quotechar='"')
    prev_date = None
    for row in reader:
        date = datetime.strptime(row["相談日"], "%Y/%m/%d")
        if prev_date is not None and (date - prev_date).days > 1:
            for i in range(1, (date - prev_date).days):
                prev_date += timedelta(days=1)
                template["data"].append({
                    "日付": prev_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "小計": 0
                })
        template["data"].append({
            "日付": date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "小計": int(row["「帰国者・接触者相談センター」受診相談件数"])
        })
        prev_date = date
    filename = 'data/querents.json'
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(template, f, indent=4, ensure_ascii=False)


def generateContacts(updated_at):
    template = {
        "date": updated_at,
        "data": []
    }
    url = "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4392/%E4%B8%80%E8%88%AC%E7%9B%B8%E8%AB%87%E4%BB%B6%E6%95%B0.csv"
    res = urllib.request.urlopen(url)
    reader = csv.DictReader(codecs.iterdecode(
        res, 'shift_jis'), delimiter=",", quotechar='"')
    prev_date = None
    for row in reader:
        date = datetime.strptime(row["相談日"], "%Y/%m/%d")
        if prev_date is not None and (date - prev_date).days > 1:
            for i in range(1, (date - prev_date).days):
                prev_date += timedelta(days=1)
                template["data"].append({
                    "日付": prev_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "小計": 0
                })
        template["data"].append({
            "日付": date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "小計": sum(int(row["「帰国者・接触者相談センター」一般相談件数（{}）".format(tp)]) for tp in ["県民", "医療機関", "行政機関", "企業", "観光・旅館", "その他"])
        })
        prev_date = date
    filename = 'data/contacts.json'
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(template, f, indent=4, ensure_ascii=False)


def generateNews():
    template = {
        "newsItems": []
    }
    url = "https://www.pref.kagawa.lg.jp/content/etc/top/ssi/rss_new.xml"
    for entry in feedparser.parse(url).entries:
        if re.search(r'^(?!.*(新型コロナウイルス感染症（COVID－19）に関する情報|香川県新型コロナウイルス対策本部等)).*(?=(コロナ|休止|休館|休業|休校|自粛|中止)).*$', entry.title) is not None:
            if len(template["newsItems"]) >= 4:
                break
            template["newsItems"].append({
                    "date": datetime.strptime(entry.updated, "%Y-%m-%d").strftime("%m/%d/%Y"),
                    "url": entry.link,
                    "text": entry.title
            })
    filename = 'data/news.json'
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(template, f, indent=4, ensure_ascii=False)


def getUpdatedAt():
    res = requests.get('https://opendata.pref.kagawa.lg.jp/dataset/359.html')
    dom = html.fromstring(res.content).xpath("//dl[@class='author']/dd[3]")
    if len(dom) != 1:
        return ""
    return datetime.strptime(dom[0].text, "%Y年%m月%d日 %H時%M分").strftime("%Y/%m/%d %H:%M")


if __name__ == "__main__":
    updated_at = getUpdatedAt()
    if updated_at != "":
        generateSummary(updated_at)
        generateQuerents(updated_at)
        generateContacts(updated_at)
    generateNews()
