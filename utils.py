#coding=utf-8

from cmd import Cmd
from random import choice
from string import lowercase
from threading import Thread
from time import sleep
import platform
import sys

def randomString(length):
    chars = []
    letters = lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)

import socket
import fcntl
import struct
 
def getLocalIp():
    local_ip = ''
    sysstr = platform.system()
    if(sysstr == 'Windows'):
        local_ip = socket.gethostbyname(socket.gethostname())
    elif(sysstr == 'Linux'):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        local_ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s','eth0'[:15]))[20:24])
    return local_ip
    
