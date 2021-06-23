import usocket
import time
import network
import gc
import Misc
from pyb import LED
import Measure
import Settings
import Server
import sys, os, pyb

if pyb.SDCard().present():
    os.mount(pyb.SDCard(), '/sd')
    sys.path[1:1] = ['/sd', '/sd/lib']

Misc.boot_display()

access_point = Server.create_access_point()
Server.serve(access_point)