
import time
import network
import config
from dht11 import DTH
from umqtt import MQTTClient
from machine import Pin
import ujson
import machine
import config

sta_if = network.WLAN(network.STA_IF)

print('connecting to network...')
sta_if.active(True)
sta_if.connect(config.WIFI_SSID, config.WIFI_PASS)
print(sta_if.isconnected())
print('network config:', sta_if.ifconfig())

# ---------------------
def sub_cb(topic, msg):
   print(msg)

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(config.SERIAL_NUMBER,
                    config.MQTT_BROKER,
                    port=config.PORT,
                    user=config.TOKEN,
                    password=config.TOPIC)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
print("MQTT IS CONNECTED")

# The MQTT topic that we publish data to
my_topic = config.TOPIC
my_temp = config.TEMPERATURE

th = DTH(Pin(15, mode=Pin.OPEN_DRAIN),0)
time.sleep(2)

while True:
    result = th.read()
    if result.is_valid():
        client.publish(topic=my_topic, msg=str(result.humidity))
        client.publish(topic=my_temp, msg=str(result.temperature))
    time.sleep(60)
