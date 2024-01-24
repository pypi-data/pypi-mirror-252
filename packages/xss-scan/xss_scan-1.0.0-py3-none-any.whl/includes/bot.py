#!/usr/bin/env python3
 
import requests
from utils import const
from utils import configure

def sendmessage(vul):

    data = {"Tname": "CVE-2023-29489", "chatid": configure.get_chatid(), "data": vul,
            "bugname": const.Data.bugname, "Priority": "Medium"}

    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.put(const.Data.api, json=data, headers=headers)
    except:
        print("Bot Error")
