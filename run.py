import usocket
import time
import network
import gc
import misc
import microdot
import measure
import settings
import Plot
import servo

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
    positions = settings.servo_positions
    
    label = request.args['label']
    date_time = request.args['date_time']
    file_name = label + '_' + date_time  + '.csv'
    
    for servo_position in positions:
        servo.position(servo_position)
        settings.blue.on()
        sample_rate = settings.sample_rate
        duration = settings.duration
        buffer = measure.measure(sample_rate, duration)
        signal_threshold = settings.signal_threshold
        settings.blue.off()
        measure.write_data(buffer, file_name, prefixes = [label, date_time, servo_position])
            
    body = web_page(request.args)
    return microdot.Response(body=body, headers=headers)


create_access_point()
app.run(debug=True, host='192.168.4.1', port=80)
    
    
    