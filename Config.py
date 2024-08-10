"""
Main program configuration
"""
config: dict = {
    "env": "dev", # "dev" or "prod"
    "appName": "Monitor",
    "defaultPassword": "MyAw3someP4ssword!", # enter the default password here
    "db": "main.db",
    "gui": {
        "warningTimes": [60*1, 60*3, 60*5]
    },
    "timeLimit": 60*45,
    "bufferSec": 5,
    "keystrokeBufferSec": 5
}
