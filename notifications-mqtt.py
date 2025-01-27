#!/usr/bin/python
import requests
import datetime
import json
from time import gmtime, strftime
from inotify_simple import INotify, flags

import os
import sys
import struct
import sqlite3
import re
import random
import time

from paho.mqtt import client as mqtt_client


broker = '192.168.178.123'
port = 1883
topic = "rundumlicht1/duration"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
eventfile = "/home/martin/.cache/xfce4/notifyd/log.sqlite"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
#    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def spin():
    client.publish(topic, "5")


con = sqlite3.connect(eventfile)
cur = con.cursor()
client = connect_mqtt()
client.loop_start()
spin()
inotify = INotify()
watch_flags = flags.MODIFY
wd = inotify.add_watch(eventfile, watch_flags)
while (True):
    inotify.read()
    res = cur.execute("SELECT summary, body FROM notifications WHERE timestamp  >= strftime('%s', 'now', '-3 second')*1000000 limit 1")
    for resline in res.fetchall():
        spin()
        body = re.sub('.*\n\n', '', resline[1])
        print(resline[0].strip() + " " + body.strip())
