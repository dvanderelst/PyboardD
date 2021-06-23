import usocket
import time
import network
import gc
import Misc
from pyb import LED
import Measure
import Settings
import HTML


Misc.boot_display()

access_point = HTML.create_access_point()
HTML.serve(access_point)