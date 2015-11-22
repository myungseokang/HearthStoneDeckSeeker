# -*- encoding : utf-8 -*-
import requests
import re
import ast
import tkinter
import operator
from collections import OrderedDict
import json
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import csv

want = input("덱 이름 : ")
BASE_URL = "http://hs.inven.co.kr/dataninfo/deck/list.ajax.php"

post_header = {
    "Host": "hs.inven.co.kr",
    "Connection": "keep-alive",
    "Content-Length": 50,
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

get_header = {
    "Host": "hs.inven.co.kr",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "kr-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4",
    "Cookie": "MOBILE_V3=NONE; _gat=1; _ga=GA1.3.1862401664.1447746835"
}

payload = {
        "subject": str(want),
        "page": "1"
    }

try:
    r = requests.post(BASE_URL,headers=post_header,data=payload)
    html_content = r.text.encode(r.encoding)
    html = BeautifulSoup(html_content, "html.parser")

    tr_list = list()
    tr_pattern = "<tr>.*?</tr>"
    r = re.compile(tr_pattern, re.DOTALL)
    tr_list = r.findall(str(html))

    idx_list = dict()
    td_pattern = "<td>[0-9]*</td>"
    pos_pattern = '<span class="positive">[0-9]*</span>'
    t = re.compile(td_pattern, re.DOTALL)
    p = re.compile(pos_pattern, re.DOTALL)

    for i in tr_list:
        se1 = t.search(i)
        se2 = p.search(i)
        j = str(se1.group()).replace("<td>","")
        td = j.replace("</td>","")
        if se2 == None:
            continue
        print(i)
        k = str(se2.group()).replace('<span class="positive">',"")
        pos = k.replace("</span>","")
        idx_list[pos]=td

    pos_list = list()
    for i in idx_list:
        pos_list.append(int(i))
    sorted_pos = sorted(pos_list, reverse=True)
    want_idx = idx_list[str(sorted_pos[0])]
    print(want_idx)

    DECK_URL = "http://hs.inven.co.kr/dataninfo/deck/view.php?idx="+want_idx

    res = requests.get(DECK_URL, headers=get_header)
    html_content = res.text.encode(res.encoding)
    html = BeautifulSoup(html_content, "html.parser")

    name_dict = dict()
    deck_pattern = 'var hsDeckSimul_data={names:{.*?}'
    r = re.compile(deck_pattern, re.DOTALL)
    name_list = r.findall(str(html))
    name_dict = name_list[0].replace("var hsDeckSimul_data={names:", "")

    cost_dict = dict()
    cost_pattern = ',costs:{.*?}'
    r = re.compile(cost_pattern, re.DOTALL)
    cost_list = r.findall(str(html))
    cost_dict = cost_list[0].replace(",costs:", "")

    rarity = {1: '모험', 2: '일반', 3: '희귀', 4: '영웅', 5: '전설'}
    rarity_list = list()
    rarity_pattern = ",rarities:{.*?}"
    r = re.compile(rarity_pattern, re.DOTALL)
    rarity_list = r.findall(str(html))
    rarity_dict = rarity_list[0].replace(",rarities:","")

    job_pattern = '<div class="deck-card-title">.*?<span id="hsDeckCardClassCount1"> </span></div>'
    r = re.compile(job_pattern, re.DOTALL)
    job = r.search(str(html))
    job = str(job.group())
    job = job.replace('<div class="deck-card-title">', "")
    job = job.replace('<span id="hsDeckCardClassCount1"> </span></div>', "")

    cnt_list = list()
    cnt_pattern = '<a hs-card="[0-9]*".*?numDeck numDeck-[1-2]"></span></a>'
    r = re.compile(cnt_pattern, re.DOTALL)
    cnt_list = r.findall(str(html))
    #print(cnt_list)

    cardname_list = list(ast.literal_eval(name_dict).values())
    cost_list = list(ast.literal_eval(cost_dict).values())
    rarity_list = list(ast.literal_eval(rarity_dict).values())

    dic = dict()
    for i in range(0, len(cardname_list)):
        st = cardname_list[i]+" "+rarity[rarity_list[i]]+"카드"
        dic[str(st)] = cost_list[i]
    dic = sorted(dic.items(), key=operator.itemgetter(1))
    print(dic)
    print(job)
    for key, val in dic:
        print(str(val)+"코"+"   "+str(key))


    '''
    root = tkinter.Tk()
    frame = tkinter.Frame(root, width=300, height=500)
    var = tkinter.StringVar()
    label = tkinter.Label(root, textvariable=var, relief=tkinter.RAISED)
    var.set(job)
    label.pack()
    root.tk.mainloop()
    '''


except:
    print("catch")