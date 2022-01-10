import urllib.request as req

import ssl
context = ssl._create_unverified_context()

import json

src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
with req.urlopen(src, context=context) as response:
    data = json.load(response)
list = data["result"]["results"]

import re
with open("data.csv", mode="w", encoding="utf-8-sig") as file:
    for item in list:
        output = []
        output.append(item["stitle"])

        address = re.split('  |區', item["address"])[1] + "區"
        checkAddress = ("中正區", "萬華區", "中山區", "大同區", "大安區", "松山區", "信義區", "士林區", "文山區", "北投區", "內湖區", "南港區")
        if(address not in checkAddress):
            continue
        output.append(address)

        output.append(item["longitude"])
        output.append(item["latitude"])
        output.append("https" + item["file"].split("https")[1])
        file.write(",".join(output) + "\n")