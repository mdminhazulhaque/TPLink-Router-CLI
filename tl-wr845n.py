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
        
    def get_token(self):
        """ get session token from router """
        r = requests.get('http://192.168.0.1/userRpm/LoginRpm.htm?Save=Save', headers=self.headers)
        match = re.search(r'http://192.168.0.1/(.*)/userRpm/Index.htm', r.text)
        
        try:
            self.token = match.group(1)
        except:
            print 'Token not found'
            sys.exit(1)

    def get_dhcp_leases(self):
        """ get list of connected peers """
        dhcp_url = 'http://192.168.0.1/' + self.token + '/userRpm/AssignedIpAddrListRpm.htm?Refresh=Refresh'
        response = requests.get(dhcp_url, headers=self.headers).text
        document = BeautifulSoup(response, 'html.parser')
        data = document.script.string.replace("var DHCPDynList = new Array(", "").replace(");", "").replace("\n", "").strip(' \t\n\r').split(", ")
        data.pop()
        info = []
        for hostname, mac, ip, lease in group(data, 4):
            info.append([mac, ip, hostname, lease])

        return tabulate(info, headers=['mac', 'ipaddr', 'hostname', 'lease'])
        
    def get_wlan_status(self):
        """ get list of wlan peers and packet statics """
        wlan_status_url = 'http://192.168.0.1/' + self.token + '/userRpm/WlanStationRpm.htm?Page=1&vapIdx='
        response = requests.get(wlan_status_url, headers=self.headers).text
        document = BeautifulSoup(response, 'html.parser')
        data = document.find_all('script')[1].string.replace("var hostList = new Array(", "").replace(");", "").replace("\n", "").strip(' \t\n\r').split(", ")
        data.pop()
        info = []
        for mac, _, received, sent, _ in group(data, 5):
            info.append([mac, humansize(received), humansize(sent)])
        return tabulate(info, headers=['mac', 'received', 'sent'])
        
if __name__ == "__main__":
    router = TL_WR845N()
    router.get_token()
    print 'dhcp_leases'
    print router.get_dhcp_leases()
    print
    print
    print 'wlan_status'
    print router.get_wlan_status()
    
