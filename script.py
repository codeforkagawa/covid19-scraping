import csv
import json
import codecs
import re
from lxml import html
import datetime
import urllib.request
import requests
import feedparser
from bs4 import BeautifulSoup

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
        date = datetime.datetime.strptime(row["相談日"], "%Y/%m/%d")
        if prev_date is not None and (date - prev_date).days > 1:
            for i in range(1, (date - prev_date).days):
                prev_date += datetime.timedelta(days=1)
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
        if row["相談日"] == '':
            continue
        date = datetime.datetime.strptime(row["相談日"], "%Y/%m/%d")
        if prev_date is not None and (date - prev_date).days > 1:
            for i in range(1, (date - prev_date).days):
                prev_date += datetime.timedelta(days=1)
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

def readCSV(f):
    result = []
    for i, line in enumerate(f.split("\n")):
        if i != 0:
            result.append(line.strip().split(","))
    return result

def generateInspectionsJson(inspections_dic,last_update):
    inspections_template = {
        "date": last_update,
        "data": {
            "県内": inspections_dic["inspections_count"],
        },
        "labels": inspections_dic["labels"]
    }
    with open("data/inspections_summary.json", "w", encoding="utf-8") as f:
        json.dump(inspections_template, f, indent=4, ensure_ascii=False)

def generateInspectionsArray():
    csv_files = [
        "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4390/%E6%A4%9C%E6%9F%BB%E4%BB%B6%E6%95%B0%EF%BC%88%E4%BB%A4%E5%92%8C2%E5%B9%B411%E6%9C%8830%E6%97%A5%E3%81%BE%E3%81%A7%EF%BC%89.csv",
        "https://opendata.pref.kagawa.lg.jp/dataset/359/resource/4946/%E6%A4%9C%E6%9F%BB%E4%BB%B6%E6%95%B0%EF%BC%88%E4%BB%A4%E5%92%8C2%E5%B9%B412%E6%9C%881%E6%97%A5%E3%81%8B%E3%82%89%EF%BC%89.csv",
    ]
    inspections_number = []
    labels = []
    patients_summary = []
    for i, url in enumerate(csv_files):
            if i == 0:
                with urllib.request.urlopen(url) as response:
                    header = ["検査日","PCR検査実施件数（環境保健研究センター）","PCR検査実施件数（医療機関）","PCR検査実施結果（陽性）","PCR検査実施結果（陰性）","抗原検査実施件数（保健所）","抗原検査実施件数（医療機関）","抗原検査実施結果（陽性）","抗原検査実施結果（陰性）"]
                    reader = csv.DictReader(codecs.iterdecode(response, 'cp932'), delimiter=",", quotechar='"', fieldnames=header)
                    for i, row in enumerate(reader):
                        if i == 0:
                            if row["PCR検査実施結果（陽性）"] != "PCR検査実施結果（陽性）":
                                raise Exception("column name is mismatch")
                            if row["抗原検査実施結果（陽性）"] != "抗原検査実施結果（陽性）":
                                raise Exception("column name is mismatch")
                            continue
                        date = datetime.datetime.strptime(row["検査日"], '%Y/%m/%d')
                        a_day_inspections_number = convertInt(
                            row["PCR検査実施件数（環境保健研究センター）"]) + convertInt(row["PCR検査実施件数（医療機関）"]) + convertInt(row["抗原検査実施件数（保健所）"]) + convertInt(row["抗原検査実施件数（医療機関）"])
                        labels.append(row["検査日"])
                        inspections_number.append(a_day_inspections_number)
                        rs = {"日付": str(date), "小計": convertInt(
                            row["PCR検査実施結果（陽性）"]) + convertInt(row["抗原検査実施結果（陽性）"])}
                        patients_summary.append(rs)
            else:
                with urllib.request.urlopen(url) as response:
                    header = ["検査日","①行政機関（PCR検査）（環境保健研究センター）","②行政機関（PCR検査）（保健所）","③行政機関（PCR検査）（高齢者施設等従事者に対する一斉検査）","④行政機関（PCR検査）（飲食店従業員に対する検査）","⑤行政機関（PCR検査）（民間検査機関）","⑥行政機関（抗原検査）（保健所）","⑦行政機関（抗原検査）（民間検査機関）","⑧医療機関検査実施報告（検査実施人数）","医療機関検査実施報告（うちPCR検査）","医療機関検査実施報告（うち抗原検査）","医療機関検査実施報告（うち行政検査）","医療機関検査実施報告（うち行政検査以外の検査）","⑨自費検査のみ実施している医療機関、検査機関からの報告","計（①＋②＋③＋④＋⑤＋⑥＋⑦＋⑧＋⑨）","陽性確定の届出"]
                    reader = csv.DictReader(codecs.iterdecode(response, 'cp932'), delimiter=",", quotechar='"', fieldnames=header)
                    for i, row in enumerate(reader):
                        if i == 0:
                            if row["陽性確定の届出"] != "陽性確定の届出":
                                raise Exception("column name is mismatch")
                            continue
                        if row["検査日"] == '':
                            continue
                        date = datetime.datetime.strptime(row["検査日"], '%Y/%m/%d')
                        a_day_inspections_number = convertInt(row["計（①＋②＋③＋④＋⑤＋⑥＋⑦＋⑧＋⑨）"])
                        labels.append(row["検査日"])
                        inspections_number.append(a_day_inspections_number)
                        rs = {"日付": str(date), "小計": convertInt(row["陽性確定の届出"])}
                        patients_summary.append(rs)
    return {"inspections_count": inspections_number, "labels": labels, "patients_summary": patients_summary}

def generatePatientsSummary(patients_summary_arr, last_update):
    patients_summary_template = {
        "date": last_update,
        "data": patients_summary_arr
    }
    with open("data/patients_summary.json", "w", encoding="utf-8") as f:
        json.dump(patients_summary_template, f, indent=4, ensure_ascii=False)

def get_patient_details(last_update):
    URL = "https://www.pref.kagawa.lg.jp/yakumukansen/kansensyoujouhou/kansen/se9si9200517102553.html"
    with urllib.request.urlopen(URL) as response:
        html = response.read().decode("utf-8")
        sp = BeautifulSoup(html, "html.parser")
        re_date_of_confirmation = re.compile(r"^(\d*)月(\d*)日（[日月火水木金土]曜日）")
        re_gender = re.compile(r"^([男女])")
        re_generation = re.compile(r"^\d*[歳代]")
        re_address = re.compile(r"^(.*[市町村都道府県].*)")
        pt_ls_d = datetime.datetime(2020, 3, 17)
        template = {
            "date": last_update,
            "data": []
        }
        for i, tag in enumerate(sp.select(".datatable tbody tr")):
            if i == 0:
                pass
            else:
                patient_data = {
                    "リリース日": "",
                    "居住地": "",
                    "年代": "",
                    "性別": "",
                    "date": "",
                }
                for i, td in enumerate(tag.select("td")):
                    txt = td.get_text(strip=True)
                    if i == 1 and re_date_of_confirmation.match(txt) == None:
                        patient_data["年代"] = txt
                        patient_data["リリース日"]: str = str(pt_ls_d)
                        patient_data["date"]: str = str(pt_ls_d.date())
                    elif re_date_of_confirmation.match(txt):
                        rp = re_date_of_confirmation.match(txt)
                        dt = datetime.datetime(
                            2020, int(rp.group(1)), int(rp.group(2)))
                        pt_ls_d = dt
                        patient_data["リリース日"]: str = str(dt)
                        patient_data["date"]: str = str(dt.date())
                    elif re_address.match(txt):
                        patient_data["居住地"] = txt
                    elif re_gender.match(txt):
                        patient_data["性別"] = txt + "性"
                    elif re_generation.match(txt):
                        patient_data["年代"] = txt
                template["data"].insert(0, patient_data)
        with open("data/patients.json", "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4, ensure_ascii=False)
def generateSummary(inspections_count,last_update):
    URL = "https://www.pref.kagawa.lg.jp/kocho/koho/kohosonota/topics/wt5q49200131182439.html"
    results = {}
    with urllib.request.urlopen(URL) as response:
        html = response.read().decode("utf-8")
        sp = BeautifulSoup(html, "html.parser")
        if len(sp.select("[summary=\"香川県の発生状況一覧\"] tbody tr")[-1].select("td")) == 6:
            for i, td in enumerate(sp.select("[summary=\"香川県の発生状況一覧\"] tbody tr")[-1].select("td")):
                txt = td.get_text(strip=True).replace("人", "")
                if i == 0:
                    results["陽性患者数"] = int(txt)
                elif i == 1:
                    results["うち直近1週間"] = int(txt)
                elif i == 2:
                    results["現在感染者数"] = int(txt)
                elif i == 3:
                    results["死亡"] = int(txt)
                elif i == 4:
                    results["退院・退所"] = int(txt)
                elif re.match(r"^＞＞（\d）(.*)", txt):
                    results["対策期のレベル"] = re.match(r"^＞＞（\d）(.*)", txt).group(1)
        else:
            print("県のサイトの更新がありました。")
    main_summary_template = {
        "date": last_update,
        "attr": "検査実施件数",
        "value": sum(inspections_count),
        "children": [
            {
                "attr": "陽性患者数",
                "value": results["陽性患者数"],
                "children": [
                    {
                        "attr": "入院中",
                        "value": results["現在感染者数"]
                    },
                    {
                        "attr": "退院",
                        "value": results["退院・退所"]
                    },
                    {
                        "attr": "死亡",
                        "value": results["死亡"]
                    },
                    {
                        "attr": "調査中",
                        "value": 0
                    }
                ]
            }
        ]
    }
    with open("data/main_summary.json", "w", encoding="utf-8") as f:
            json.dump(main_summary_template, f, indent=4, ensure_ascii=False)

def getUpdatedAt():
    res = requests.get('https://opendata.pref.kagawa.lg.jp/dataset/359.html')
    dom = html.fromstring(res.content).xpath("//dl[@class='author']/dd[3]")
    if len(dom) != 1:
        return ""
    return datetime.datetime.strptime(dom[0].text, "%Y年%m月%d日 %H時%M分").strftime("%Y/%m/%d %H:%M")

def convertInt(digit):
    if digit == "ー" or digit == "":
        return 0
    return int(digit)

if __name__ == "__main__":
    # 県のサイトからのスクレイピングの最終更新日はこちらを使用
    LAST_UPDATE = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M')
    # オープンデータから取得したファイルの最終更新日はこちらを使用
    updated_at = getUpdatedAt()
    if updated_at != "":
        generateQuerents(updated_at)
        generateContacts(updated_at)
    summary_inspections = generateInspectionsArray()
    get_patient_details(LAST_UPDATE)
    generateSummary(summary_inspections["inspections_count"],LAST_UPDATE)
    generateInspectionsJson(summary_inspections,LAST_UPDATE)
    generatePatientsSummary(summary_inspections["patients_summary"],LAST_UPDATE)
    # generateNews()
