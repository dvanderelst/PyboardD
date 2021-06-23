

import network

wl_ap = network.WLAN(1)
wl_ap.config(essid='PYBD')          # set AP SSID
wl_ap.config(password='test')   # set AP password
wl_ap.config(channel=6)             # set AP channel
wl_ap.active(1)      


from microdot import Microdot, Response

app = Microdot()

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
def hello(request):
    return Response(body=htmldoc, headers={'Content-Type': 'text/html'})


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


app.run(debug=True)
