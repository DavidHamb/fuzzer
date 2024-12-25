#!/usr/bin/python3
import requests
import re
import time
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("payloads")
parser.add_argument("method")
parser.add_argument("get_parameter", nargs="?") # nargs because this argument is optionnal
args = parser.parse_args()

wordlist = open(args.payloads, 'r')
payloads = wordlist.readlines()
wordlist.close()

url = args.url
method = args.method
r = requests.get(url)
timenow = str(datetime.now()).replace(" ", "_")
filename = "./output/fuzzing_result_" + timenow + ".txt"
f = open(filename, "a")

# handle fuzzing via POST method
if method == "post":
    params = re.findall('(?<=name=")\w+(?=")', r.text) 
    n = 0
    for payload in payloads:
        n = n + 1
        payload = payload[0:len(payload)-1]
        for param in params:
            p = requests.post(url, data={param: payload})
            result = str(p.status_code) + " " + str(len(p.text)) + " " + str(p.elapsed.total_seconds()) + " " + url + "?" + param + "=" + payload
            print(str(n) + " out of  " + str(len(payloads)) + " - " + result)
            time.sleep(1)
            f.write(result + "\n")
    f.close()
    print("Results stored in output folder")

# handle fuzzing via url (e.g. directory listing ...)
elif method == "get":
    get_parameter = args.get_parameter
    if get_parameter:
        n = 0
        for payload in payloads:
            n = n + 1
            payload = payload[0:len(payload)-1]
            g = requests.get(url + "?" + get_parameter + "=" + payload)
            result = str(g.status_code) + " " + str(len(g.text)) + " " + str(g.elapsed.total_seconds()) + " " + url + "?" + get_parameter + "=" + payload
            print(str(n) + " out of  " + str(len(payloads)) + " - " + result)
            f.write(result + "\n")
        f.close()
        print("Results stored in output folder")
    else:
        print("Please specify a parameter name")

else:
    print("Choose a method 'post' or 'get'")


