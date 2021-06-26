import usocket
import time
import network
import gc
import Misc
import microdot
import Measure
import Settings
import Plot

def web_page(input_values={}):
    f = open('form.html','r')
    html = f.read()
    f.close()
    if 'date_time' in input_values: html = html.replace('xx_date_time_xx', input_values['date_time'])
    if 'label' in input_values: html = html.replace('xx_label_xx', input_values['label'])
    if 'comment' in input_values: html = html.replace('xx_comment_xx', input_values['comment'])
    return html


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



headers={'Content-Type': 'text/html'}
gc.collect()

app = microdot.Microdot()

@app.route('/')
def hello(request):
    gc.collect()
    return microdot.Response(body=web_page(), headers=headers)


@app.route('/form_action')
def process_form(request):
    gc.collect()
    Settings.