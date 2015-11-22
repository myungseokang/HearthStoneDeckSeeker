# -*- encoding : utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import csv

#want = input("덱 이름 : ")
#print(want)
want = ""
BASE_URL = "http://hs.inven.co.kr/dataninfo/deck/list.ajax.php"

header = {
        "Host": "hs.inven.co.kr",
        "Connection": "keep-alive",
        "Content-Length": 42,
        "Origin": "https://hs.inven.co.kr",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "text/html, */*; q=0.01",
        "Referer": "https://hs.inven.co.kr/dataninfo/deck/",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "kr-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4",
        "Cookie": "MOBILE_V3=NONE; _gat=1; _ga=GA1.3.1862401664.1447746835"
    }



payload = {
        "subject": "용사제",
        "page": "1"
    }

try:
    r = requests.post(BASE_URL,headers=header,data=payload)
    html_content = r.text.encode(r.encoding)
    html = BeautifulSoup(html_content, "html.parser")
    span_list = html.find_all("span","positive")
    pos_list = list()
    positive_list = list()
    for i in span_list:
        pos_list.append(str(i).replace('<span class="positive">', ""))

    for i in pos_list:
        positive_list.append(str(i).replace("</span>", ""))
except ConnectionError:
    print("ConectionError")
except:
    print("catch")