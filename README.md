# TL-WR845N-API

Simple HTTP API for remote data polling or controlling TL-WR845N router (might work with other TPLink routers!)

## Available Functions

* get_dhcp_leases
* get_wlan_status

## Sample Result

```
$ python tl-wr845n.py
dhcp_leases
mac                  ipaddr           hostname                    lease
-------------------  ---------------  --------------------------  -----------
"02-5C-24-FD-52-5E"  "192.168.0.200"  "minhaz-desktop"            "Permanent"
"8B-8C-28-6B-08-EE"  "192.168.0.201"  "android-3f5ff12ab477dc20"  "Permanent"
"18-A6-F7-0D-48-5D"  "192.168.0.103"  "DESKTOP-82RHDDV"           "01:18:34"
"D8-5D-E2-36-01-55"  "192.168.0.100"  "DESKTOP-2VROC92"           "01:32:07"
"10-02-B5-66-27-F9"  "192.168.0.105"  "vipnoc-laptop"             "01:51:39"
"B4-52-7E-65-2A-25"  "192.168.0.101"  "android-df9862b973a1b189"  "01:35:20"
"32-D4-20-64-BC-7D"  "192.168.0.106"  "android-b008e6d4e99098ea"  "01:49:41"
"2D-C1-00-EB-F4-62"  "192.168.0.104"  "android-742d70a6df57f731"  "01:27:09"

wlan_status
mac                    received    sent
-------------------  ----------  ------
"18-A6-F7-0D-48-5D"      402222  438864
"8B-8C-28-6B-08-EE"       29012   40326
"02-5C-24-FD-52-5E"      117266  178925
"D8-5D-E2-36-01-55"      128861  302347
"32-D4-20-64-BC-7D"       48997  103683
"2D-C1-00-EB-F4-62"        3187    2690
```


## TODO

* Add more functions to get status updates
* Map mac address with status updates
* Cleanup code
* Create a webui (AngularJS perhaps!)
