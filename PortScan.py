#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import threading
import re

lock = threading.Lock()
openNum = 0
threads = []

def portScanner(host,port):
    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        print('[+] %d open' % port)
        lock.release()
        s.close()
    except:
        pass

def main():
    host=input("Please input IPv4: ")
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", host):
        print ("IP is OK")
    else:
        print ("IPv4 format is invaild")
        exit()
    minPort=int(input("Please input Min of Ports: "))
    if(minPort<0):
        print("MinPort can't less than zero")
        exit()
    MaxPort=int(input("Please input Max of Ports(Max is 65536): "))
    if(MaxPort>65537):
        print("MaxPort can't bigger than 65536")
        exit()
    print('[*] scan '+host+' Start!\n')
    setdefaulttimeout(1)
    for p in range(minPort,MaxPort):
        t = threading.Thread(target=portScanner,args=(host,p))
        threads.append(t)
        t.start()     
    for t in threads:
        t.join()
    print('\n[*] scan Over!Find %d open ports ' % (openNum))

if __name__ == '__main__':
    main()