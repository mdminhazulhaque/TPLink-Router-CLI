#!/usr/bin/env python2

# Written by
# Md. Minhazul Haque, 2017, GPL, mdminhazulhaque@gmail.com

import re
from bs4 import BeautifulSoup
import requests
import md5
import binascii
import base64
import urllib
import argparse

group = lambda t, n: zip(*[t[i::n] for i in range(n)])

class TPLinkRouter:
    URL_LOGIN = 'userRpm/LoginRpm.htm?Save=Save'
    URL_LOGOUT = '/userRpm/LogoutRpm.htm'
    URL_CLIENT_LIST = '/userRpm/AssignedIpAddrListRpm.htm?Refresh=Refresh'
    URL_WLAN_STAT = '/userRpm/WlanStationRpm.htm?Page=1&vapIdx='
    
    @staticmethod
    def humansize(bytes):
        nbytes = int(bytes) * 1024
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])
    
    @staticmethod
    def hex_md5(password):
        m = md5.new()
        m.update(password)
        return binascii.hexlify(m.digest())
    
    @staticmethod
    def basic_auth(username, password):
        auth = username + ":" + TPLinkRouter.hex_md5(password)
        b64auth = base64.b64encode(auth)
        return urllib.quote('Basic ' + b64auth)

    def __init__(self, address="192.168.0.1", username="admin", password="admin"):
        auth = TPLinkRouter.basic_auth(username, password)
        self.address = 'http://' + address + '/'
        self.headers = {
            'Cookie': 'Authorization=' + auth,
            'Referer': self.address
        }
        self.get_token()
        
    def get_token(self):
        for try_count in range(3):
            try:
                r = requests.get(self.address + self.URL_LOGIN, headers=self.headers)
                self.token = r.text.split("/")[3]
                assert re.match('^[A-Z0-9]{16}$', self.token) == True
            except:
                if try_count == 3:
                    os.exit(1)
    
    @staticmethod
    def replace_by(data, key):
        data = data.replace("var " + key + " = new Array(", "")\
                .replace(");", "")\
                .replace("\n", "")\
                .replace("\"", "")\
                .strip(' \t\n\r')\
                .split(", ")
        data.pop()
        return data
            
    def get_dhcp_clients(self):
        dhcp_url = self.address + self.token + self.URL_CLIENT_LIST
        response = requests.get(dhcp_url, headers=self.headers).text
        document = BeautifulSoup(response, 'html.parser')
        data = TPLinkRouter.replace_by(document.script.string, "DHCPDynList")
        info = {}
        for hostname, mac, ip, lease in group(data, 4):
            info[mac] = [hostname, ip]
        return info
        
    def get_wlan_stat(self):
        wlan_status_url = self.address + self.token + self.URL_WLAN_STAT
        response = requests.get(wlan_status_url, headers=self.headers).text
        document = BeautifulSoup(response, 'html.parser')
        data = TPLinkRouter.replace_by(document.find_all('script')[1].string, "hostList")
        return data
    
    def merge_client_stat(self, sort=False, human=True):
        mac_map = self.get_dhcp_clients()
        data = self.get_wlan_stat()
        info = []
        for mac, _, received, sent, _ in group(data, 5):
            try:
                name = mac_map[mac][0]
                ip = mac_map[mac][1]
                info.append([ip, mac, name, int(received), int(sent)])
            except:
                info.append(["Unknown", mac, "Unknown", int(received), int(sent)])            
        
        if sort:
            info = sorted(info, key = lambda x: x[3]+x[4], reverse=True)
            
        if not human:
            for entry in info:
                entry[3] = TPLinkRouter.humansize(entry[3])
                entry[4] = TPLinkRouter.humansize(entry[4])
        return info
    
    @staticmethod
    def macbind_clients(mac_map_file, stat):
        mac_map = {
            "00-11-22-33-44-55": "Foo",
            "AA-BB-CC-DD-EE-FF": "Bar"
        }
        with open(mac_map_file) as file:
            for line in file:
                mac, name = line.strip().split(" ", 1)
                mac_map[mac] = name
                
        for entry in stat:
            try:
                name = mac_map[entry[1]]
                entry[2] = name
            except:
                pass
        return stat
        
    def __del__(self):
        logout_url = self.address + self.token + self.URL_LOGOUT
        response = requests.get(logout_url, headers=self.headers).text
        if "Authorization=;path=/" in response:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TPLink Router CLI Client", add_help=False)
    parser.add_argument('-h', dest='host', action="store", default="192.168.0.1", type=str)
    parser.add_argument('-u', dest='user', action="store", default="admin", type=str)
    parser.add_argument('-p', dest='pswd', action="store", default="admin", type=str)
    parser.add_argument('-s', dest='sort', action="store_true", default=False)
    parser.add_argument('-b', dest='bytes', action="store_true", default=False)

    args = parser.parse_args()
    
    router = TPLinkRouter(address=args.host, username=args.user, password=args.pswd)
    stat = router.merge_client_stat(human=args.bytes, sort=args.sort)
    stat = TPLinkRouter.macbind_clients("macbind.txt", stat)
    
    from tabulate import tabulate
    print tabulate(stat, headers=['ip', 'mac', 'name', 'received', 'sent'])
    
