#!/usr/bin/python

import sys
import time
import paho.mqtt.client as mqtt
from vocabulary.Config import MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD

#publishResult(user, "Latein","Deklinieren", settingDeklination, "Pauken",  note, duration, gesamt, fehler)
def publishResult(user, language, type, subtype, subsubtype, note, duration, gesamt, fehler):
    client = mqtt.Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # /vocabulary/anton/latein/deklinieren/a-Deklination/pauken/note
    # /vocabulary/anton/latein/deklinieren/a-Deklination/pauken/dauersekunden
    # /vocabulary/anton/latein/deklinieren/a-Deklination/pauken/gesamt
    # /vocabulary/anton/latein/deklinieren/a-Deklination/pauken/fehler
    print(fehler)
    S = "/"
    topic = "vocabulary/"+user+S+language+S+type+S+subtype+S+subsubtype+S
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.publish(topic+"note", note)
    client.publish(topic+"dauer", duration)
    client.disconnect()

    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.publish(topic+"gesamt", gesamt)
    client.publish(topic+"fehler", fehler)
    client.disconnect()
    

#publishResult("andreas","Latein","deklinieren", "a-Deklinination", "Pauken",  3, 360, 30, 4)