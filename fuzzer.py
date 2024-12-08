#!/usr/bin/python3
import requests
import re
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("payloads")
args = parser.parse_args()

wordlist = open(args.payloads, 'r')
payloads = wordlist.readlines()
wordlist.close()

url = args.url
r = requests.get(url)
params = re.findall('(?<=name=")\w+(?=")', r.text) 

for payload in payloads:
    payload = payload[0:len(payload)-1]
    for param in params:
        p = requests.post(url, data={param: payload})
        print(str(p.status_code) + " " + str(len(p.text)) + " " + str(p.elapsed.total_seconds()) + " " + url + "?" + param + "=" + payload)
        time.sleep(1)


