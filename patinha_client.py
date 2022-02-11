# Cliente TCP para ESP8266

import network
import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = "hello"

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('raspi-webgui','ChangeMe')
        while not wlan.isconnected():
            pass
        print('network config:', wlan.ifconfig())


def patinha_Setup():
    do_connect()
    sock.connect(('10.3.141.1', 5005))
  
def patinha_Loop():
    while True:
      sock.write(data.encode())
      sleep(1)


patinha_Setup()

patinha_Loop()








