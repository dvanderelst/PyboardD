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


gc.collect()
headers={'Content-Type': 'text/html'}
app = microdot.Microdot()
gc.collect()

@app.route('/')
def hello(request):
    gc.collect()
    return microdot.Response(body=web_page(), headers=headers)


@app.route('/form_action')
def process_form(request):
    gc.collect()
    positions = settings.servo_positions
    data_sep = settings.data_sep
    
    label = request.args['label']
    date_time = request.args['date_time']
    comment = request.args['comment']
    file_name = label + '_' + date_time  + '.csv'
    
    for servo_position in positions:
        servo.position(servo_position)
        settings.blue.on()
        sample_rate = settings.sample_rate
        duration = settings.duration
        buffer = measure.measure(sample_rate, duration)
        signal_threshold = settings.signal_threshold
        settings.blue.off()
        comment = comment.replace(data_sep, '')
        if len(label) > 0: measure.write_data(buffer, file_name, prefixes = [label, comment ,date_time, servo_position], sep=data_sep)
            
    body = web_page(request.args)
    return microdot.Response(body=body, headers=headers)


create_access_point()
gc.collect()
misc.boot_display()
app.run(debug=True, host='192.168.4.1', port=80)