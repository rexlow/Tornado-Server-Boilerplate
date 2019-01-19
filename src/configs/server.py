#!/usr/bin/python3

server_configs = {
    "host": "0.0.0.0",
    "port": 8080,
    "max_workers": 1000,
    "debug": False
}

default_get_response = '''
    <html style="height: 100%; display: table; margin: auto;">
        <body style="height: 100%; display: table-cell; vertical-align: middle;">
            <h1 style="font-family: 'Raleway', sans-serif; font-weight: 100;">
                Tornado Server Boilerplate
            </h1>
        </body>
    </html>
'''