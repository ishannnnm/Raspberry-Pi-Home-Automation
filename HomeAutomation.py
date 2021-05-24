import paho.mqtt.client as mqtt
import os, urllib.parse
import time
import RPi.GPIO as gpio
from urllib.request import urlopen
import Adafruit_DHT


relay1 = 7
relay2 = 8
relay3 = 10
relay4 = 11
buz_pin = 13
sensor = Adafruit_DHT.DHT11
dhtpin = 23

time.sleep(15)
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(relay1, gpio.OUT)
gpio.setup(relay2, gpio.OUT)
gpio.setup(relay3, gpio.OUT)
gpio.setup(relay4, gpio.OUT)
gpio.output(relay1, gpio.LOW)
gpio.output(relay2, gpio.LOW)
gpio.output(relay3, gpio.LOW)
gpio.output(relay4, gpio.LOW)
gpio.setup(buz_pin, gpio.OUT)




    
def on_connect(self, mosq, obj, rc):
    print ("on_connect:: Connected with result code "+ str ( rc ) )
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print ("on_message:: this means  I got a message from brokerfor this topic")
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if(msg.topic == "relay1"):
        if (msg.payload.decode("utf-8") == "on"):
            print("Relay1 On")
            gpio.output(relay1, gpio.HIGH)
        elif (msg.payload.decode("utf-8")  == "off"):
            print("Relay1 Off")
            gpio.output(relay1, gpio.LOW)
    if(msg.topic == "relay2"):
        if (msg.payload.decode("utf-8") == "on"):
            print("Relay2 On")
            gpio.output(relay2, gpio.HIGH)
        elif (msg.payload.decode("utf-8")  == "off"):
            print("Relay2 Off")
            gpio.output(relay2, gpio.LOW)
    if(msg.topic == "relay3"):
        if (msg.payload.decode("utf-8") == "on"):
            print("Relay3 On")
            gpio.output(relay3, gpio.HIGH)
        elif (msg.payload.decode("utf-8")  == "off"):
            print("Relay3 Off")
            gpio.output(relay3, gpio.LOW)
    if(msg.topic == "relay4"):
        if (msg.payload.decode("utf-8") == "on"):
            print("Relay4 On")
            gpio.output(relay4, gpio.HIGH)
        elif (msg.payload.decode("utf-8")  == "off"):
            print("Relay4 Off")
            gpio.output(relay4, gpio.LOW)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("This means broker has acknowledged my subscribe request")
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


client = mqtt.Client()

client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe

client.on_log = on_log


client.username_pw_set("dycgxiix", "WETNQObOMCvL")

client.connect('farmer.cloudmqtt.com', 12135, 60)



client.loop_start()
client.subscribe("relay1")
client.subscribe("relay2")
client.subscribe("relay3")
client.subscribe("relay4")

print("System Started")
gpio.output(buz_pin, gpio.HIGH)
time.sleep(0.250)
gpio.output(buz_pin, gpio.LOW)
time.sleep(0.250)
gpio.output(buz_pin, gpio.HIGH)
time.sleep(0.250)
gpio.output(buz_pin, gpio.LOW)
time.sleep(0.250)

while True:
    time.sleep(5)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtpin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        client.publish("temp", temperature)
        client.publish("hum", humidity)
    else:
        print('Failed to get reading. Try again!')
    
