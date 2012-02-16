#coding=utf-8

from xmlrpclib import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import lowercase
from server import Node,UNHANDLED
from threading import Thread
from time import sleep

import sys

def randomString(length):
    chars = []
    letters = lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)
