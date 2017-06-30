# TL-WR845N-API

Simple HTTP API for remote data polling or controlling TL-WR845N router (might work with other TPLink routers!)

## Sample Result

```
$ python tl-wr845n.py
ip               mac                  name                        received    sent     
---------------  -------------------  --------------------------  ----------  ---------
"192.168.0.108"  "36-01-55-D8-5D-E2"  "DESKTOP-2V44CC92"          5.9 GB      7.22 GB  
"192.168.0.103"  "52-7E-65-B4-2A-25"  "android-df9862b973a1b189"  197.33 MB   267.36 MB
"192.168.0.101"  "44-15-6F-F0-99-BF"  "rakib38s-iPhone"           4.31 MB     1.95 MB  
"192.168.0.106"  "74-F0-6D-31-D6-B0"  "mew-laptop"                62.92 MB    66.73 MB 
"192.168.0.200"  "24-FD-5C-52-5E-02"  "Minhaz-PC"                 57.75 MB    73.16 MB 
"192.168.0.201"  "ED-1B-82-24-38-A4"  "Minhaz-MI5"                1.57 MB     1.01 MB  
```

## TODO

- [ ] Add more functions to get status updates
- [x] Map mac address with status updates
- [x] Human readable up/down data statistics
- [ ] Cleanup code
- [ ] Create an webui (AngularJS perhaps!)
