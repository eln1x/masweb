#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ahmad Mahfouz'
__version__ = "1.0"
__email__='n1x.osx#icloud.com'
__status__='Developemnt'
__license__ ='GNU'
__version__ = "3"
# MasWeb  ( Common web ports )
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
try:

	import requests
	from bs4 import BeautifulSoup
	from Queue import Queue
	from threading import Thread,Lock
	from datetime import datetime
	import threading
	import time
	import sys
	import argparse
	import random
	import json
except:
	print "[!] Error: please install the requirments , pip install -r requirements.txt"
	import sys
	sys.exit(0)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


banner = """
.___  ___.      ___           _______.____    __    ____  _______ .______   
|   \/   |     /   \         /       |\   \  /  \  /   / |   ____||   _  \  
|  \  /  |    /  ^  \       |   (----` \   \/    \/   /  |  |__   |  |_)  | 
|  |\/|  |   /  /_\  \       \   \      \            /   |   __|  |   _  <  
|  |  |  |  /  _____  \  .----)   |      \    /\    /    |  |____ |  |_)  | 
|__|  |__| /__/     \__\ |_______/        \__/  \__/     |_______||______/  
                                                                            

                                                                      Version 1.0
								      Author: Ahmad Mahfouz @eln1x
"""
NOTICE = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

print OKBLUE+ banner + ENDC


parser = argparse.ArgumentParser(description="""titler list domain titles""" )		
parser.add_argument("-d", "--domains", action='store',  dest='domain', help="target domain name")
# parser.add_argument("-p", "--ports", dest='ports' ,help="ports, in list" ,action="store", default=port_list)
parser.add_argument("-t", "--threads", dest="threads", help="number of threads", type=int, default=10)
parser.add_argument("-x", "--timeout", dest='timeout' ,help="connection timeout", type=int, default=5)

args = parser.parse_args()


domains = args.domain
# port = args.port

threads = args.threads
timeout = args.timeout
# debug = args.debug
ports = [80,443,8080,8000,8443,8081,9090,9080]

usage = """
[!] Usage example
	python masweb.py --domains list.txt  -x 5
"""

if not domains:

	print FAIL + usage + ENDC
	sys.exit(1)

f = open(domains,'r')

domains_list = []
for line in f.readlines():
	domains_list.append(line.strip())





# print """%s
# [!] Target Domain : %s
# [!] Target Method : %s
# [!] Target Port   : %s
# [!] Target Subnet : %s
# [!] Target Timout : %s 
# [!] Total Threads : %s
# [!] Total IPs     : %s      
# [!] Debug Status  : %s                                                         
# %s"""  %(OKBLUE,domains,method,port,subnet,timeout,threads,len(ips),debug,ENDC)


print "%s[+] Masweb Started at %s%s" %(NOTICE,datetime.now(),ENDC)

# captured = []
q = Queue(maxsize=0)
lock = Lock()

def Result(domain,port,status_code,version,redirect,title,hit,powered,length):



	lock.acquire()
	sys.stdout.write("\r")
	sys.stdout.flush()


	target = "%s:%s" %(domain,port)
	if status_code >= 200 and status_code < 300:
		msg = "[-] %s Ok: %s - Banner: %s - Title: %s -  Powered: %s Length: %s" %(status_code,target,version,title,powered,length)
	elif status_code >= 300 and status_code < 400:
		msg = "[-] %s RD: %s - Banner: %s - Length: %s - Location: %s - Hit: %s" %(status_code,target,version,length,redirect,hit)
	elif status_code >= 400 and status_code < 500:
		msg = "[-] %s NF: %s - Banner: %s - Length: %s" %(status_code,target,version,length)
	elif status_code >= 500 and status_code < 600:
		msg = "[-] %s ER: %s - Banner: %s - Length: %s" %(status_code,target,version,length)
	else:
		print "[!] %s XX: %s - Banner: %s - Length: %s" %(status_code,target,version,length)
	
	if powered is not None or status_code == 200:
		print OKGREEN + msg + ENDC
	else:
		print msg
	lock.release()
	return True

def Grep(domain,port):



	if str(443) in str(port) :
		method = "https"
	else:
		method = "http"
	try:

            	r = requests.get('%s://%s:%s/' %(method,domain,port),
                    		headers={
                            		'host': domain,
                            		'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                            	},
                    		timeout=timeout,
                    		verify=False,
                    		allow_redirects = False,
                    # proxies=dict(http='http://127.0.0.1:8080')

                    	)


	except requests.exceptions.ConnectionError:
		return False

	except requests.exceptions.TooManyRedirects:
		return False

	except requests.exceptions.ReadTimeout:		
		return False

	except requests.exceptions.InvalidURL:
		return False
	else:

		try:
			version = r.headers['Server']
		except:
			version = None

		if len(r.text)>10:
			soup = BeautifulSoup(r.text, 'html.parser')

			try:
				title = soup.find('title').text.encode('utf-8').strip()
			except:
				title = None
		else:
			title = None

		status_code = r.status_code
		length = len(r.text)

		try:
			redirect = r.headers['Location']

		except:
			redirect = None

		try:
			powered = r.headers['X-Powered-By']
		except:
			powered = None

		try: 
			hit = r.headers['X-Cache']
		except:
			hit = None
		Result(domain,port,status_code,version,redirect,title,hit,powered,length)


	
def Operator(domain,ports):

	for port in ports:
		art = ['/','\\','-']
		sys.stdout.write("\r%s[+] Masweb test Target.. %s %s:%s %s" %(OKGREEN, domain, port,random.choice(art),ENDC))
		sys.stdout.flush()
		Grep(domain, port)
	

	return True

def FireThreads(q):
	while True:
		domain= q.get()
		Operator(domain,ports)
		q.task_done()


if len(domains_list) == 0:
	print FAIL + "[!] Really!!, i have nothing to scan, going to die "+ ENDC
	sys.exit(0)

for domain in domains_list:
	q.put(domain)




for i in range(threads):
	worker = Thread(target=FireThreads, args=(q,))
	worker.setDaemon(True)
	worker.start()

q.join()
print ""
print "%s[+] Titles Finished at %s%s" %(NOTICE,datetime.now(),ENDC)
