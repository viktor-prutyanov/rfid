#!/usr/bin/python3

import os, sys
from sllurp import llrp
from twisted.internet import reactor, task
import logging
from time import sleep
from threading import Timer
import serial
import time
import signal
import sys

if len(sys.argv) != 3:
    exit("usage: {0} ip uart_nr".format(sys.argv[0]))

with open('users.txt', 'r') as f:
    users_l = f.readlines()

users = {}

for u in users_l:
    l = u.rstrip("\n").split(" ")
    users[l[0]] = l[1]

s = serial.Serial("/dev/ttyACM" + sys.argv[2], 115200)

products = {}
with open('labels.txt', 'r') as f:
    labels = f.readlines()
    for l in labels:
        p = l.split("\n")[0].split(" ")
        products[p[1]] = [p[0], 0]
print(products)

logging.getLogger().setLevel(logging.DEBUG)

def shutdown(factory):
    return factory.politeShutdown()

#def t_task():
#    #os.system("clear")
#    print(products)
#
#task.LoopingCall(t_task).start(1.0)

def cb(tagReport):
    tags = tagReport.msgdict['RO_ACCESS_REPORT']['TagReportData']
    if len(tags) == 1:
        if 'EPC-96' in tags[0]:
            uid = tags[0]['EPC-96'].decode('ascii')
            products[uid][1] = time.time()
            #print(products)

def sThread():
    while True:
        uid_str = s.readline().decode("ascii").replace(" ", "").rstrip("\n").rstrip("\r")
        if len(uid_str) != 0:
            print(users[uid_str], uid_str)
            print(products)
            t = time.time()
            for p in products:
                print(p)

factory = llrp.LLRPClientFactory(report_every_n_tags=1, tx_power=20)
factory.addTagReportCallback(cb)
reactor.connectTCP(sys.argv[1], llrp.LLRP_PORT, factory)
reactor.addSystemEventTrigger('before', 'shutdown', shutdown, factory)
reactor.callInThread(sThread)
reactor.run()
