context = 'field'

########################################################################################
# FIELD CONTEXT
########################################################################################
def take_measurement(label, comment, date_time, servo_position):
    servo.position(servo_position)
    settings.blue.on()
    sample_rate = settings.sample_rate
    duration = settings.duration
    data_sep = settings.data_sep
    buffer = measure.measure(1, sample_rate, duration)
    signal_threshold = settings.signal_threshold
    settings.blue.off()
    if len(label) > 0: measure.write_data(buffer, file_name, prefixes = [label, comment ,date_time, servo_position], sep=data_sep)


if context == 'field':
    
    import time
    import gc
    import misc
    import microdot
    import measure
    import settings
    import servo
    import server
    import sys
    import os
    import pyb
    
    gc.collect()
    settings.green.on()
    settings.red.on()
    sd_card = pyb.SDCard()
    if sd_card.present(): os.mount(sd_card, '/sd')
    time.sleep(1)
    settings.green.off()
    settings.red.off()

    gc.collect()
    headers={'Content-Type': 'text/html'}
    app = microdot.Microdot()

    gc.collect()
    @app.route('/')
    def hello(request):
        gc.collect()
        return microdot.Response(body=server.web_page(), headers=headers)


    @app.route('/form_action')
    def process_form(request):
        gc.collect()
        positions = settings.servo_positions
        repeats = settings.repeats
        
        label = request.args['label']
        date_time = request.args['date_time']
        comment = request.args['comment']
        comment = comment.replace(data_sep, '')

        file_name =  '/sd/' + label + '_' + date_time  + '.csv'
        
        for servo_position in positions:
            for repeat in range(repeats):
                take_measurement(label, comment, date_time, servo_position)
               
        
        contents = os.listdir('/sd/')
        contents_list = open('sd_contents.txt','w')
        contents_list.write(str(contents))
        contents_list.close()
        
        
        body = server.web_page(request.args)
        return microdot.Response(body=body, headers=headers)


    server.create_access_point()
    gc.collect()
    misc.boot_display1()
    app.run(debug=True, host='192.168.4.1', port=80)


########################################################################################
# ROBOT CONTEXT
########################################################################################

if context == 'robot':
    import usocket
    import time
    import gc
    import misc
    import measure
    import settings
    import server
    import ujson
        
    green = settings.green
    blue = settings.blue
    red = settings.red

    gc.collect()
    misc.boot_display2()
    
    green.on()
    red.on()
    server.connect2wifi()
    time.sleep(1)
    green.off()
    red.off()
    while True:
        green.on()
        data_server = server.Server()
        
        message = data_server.receive_data()
        message = message.split(settings.data_sep)
        first = int(message[0])
        second = int(message[1])
        sample_rate = int(message[2])
        duration = int(message[3])
        
        green.off()
        blue.on()
        buffer = measure.measure_both(first, second, sample_rate, duration)
        blue.off()

        buffer = ujson.dumps(buffer)
        data_server.send_data(buffer)
        
        data_server.disconne