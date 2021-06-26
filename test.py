import usocket
import time
import network
import gc
import Misc
import microdot
import Measure
import Settings
import Plot


def create_access_point():
    access_point = network.WLAN(1)
    access_point.config(essid='PYBD')          # set AP SSID
    access_point.config(password='pybd0123')   # set AP password
    access_point.config(channel=6)             # set AP channel
    access_point.active(1)                     # enable the AP
    while access_point.isconnected() == False: pass
    print('Connection successful')
    print(access_point.ifconfig())
    return access_point




app = microdot.Microdot()




@app.route('/')
def hello(request):
    return microdot.Response(body=htmldoc, headers={'Content-Type': 'text/html'})


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


create_access_point()
app.run(debug=True, host='127.0.0.0', port=80)
