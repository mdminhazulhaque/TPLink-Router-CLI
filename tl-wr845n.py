#!/usr/bin/env python

# Written by
# Md. Minhazul Haque, 2017, GPL, mdminhazulhaque@gmail.com

import requests
import re
import sys

from bs4 import BeautifulSoup
from tabulate import tabulate

group = lambda t, n: zip(*[t[i::n] for i in range(n)])

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

class TL_WR845N:
    def __init__(self):
        self.headers = {
            # TODO Generate basic authentication from username password using JS core_md5 and other functions
            'Cookie': 'Authorization=Basic%20YWRtaW46MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM%3D',
            'Referer': 'http://192.168.0.1/'
        }
        self.get_token()
        
    def get_token(self):
        """ get session token from router """
        r = requests.get('http://192.168.0.1/userRpm/LoginRpm.htm?Save=Save', headers=self.headers)
        match = re.search(r'http://192.168.0.1/(.*)/userRpm/Index.htm', r.text)
        
        for try_count in range(3):
            try:
                self.token = match.group(1)
                return
            except:
                pass
        
        print 'Token not found'
        sys.exit(1)

    def client_mac(self):
        """ get list of connected peers """
        dhcp_url = 'http://192.168.0.1/' + self.token + '/userRpm/AssignedIpAddrListRpm.htm?Refresh=Refresh'
        response = requests.get(dhcp_url, headers=self.headers).text
        document = BeautifulSoup(response, 'html.parser')
        data = document.script.string.replace("var DHCPDynList = new Array(", "").replace(");", "").replace("\n", "").strip(' \t\n\r').split(", ")
        data.pop()
        info = {}
        for hostname, mac, ip, lease in group(data, 4):
            info[mac] = [hostname, ip]
        return info
        
    def client_stat(self):
        """ get list of wlan peers and packet statics """        
        mac_map = self.client_mac()
        
        wlan_status_url = 'http://192.168.0.1/' + self.token + '/userRpm/WlanStationRpm.htm?Page=1&vapIdx='
        response = requests.get(wlan_status_url, headers=self.headers).text
        document = BeautifulSoup(response, 'html.parser')
        data = document.find_all('script')[1].string.replace("var hostList = new Array(", "").replace(");", "").replace("\n", "").strip(' \t\n\r').split(", ")
        data.pop()
        info = []
        for mac, _, received, sent, _ in group(data, 5):
            name = mac_map[mac][0]
            ip = mac_map[mac][1]
            info.append([ip, mac, name, humansize(received), humansize(sent)])
            
        return info
        
if __name__ == "__main__":
    router = TL_WR845N()
    stat = router.client_stat()    
    print tabulate(stat, headers=['ip', 'mac', 'name', 'received', 'sent'])
    
    
