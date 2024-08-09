"""
Main program configuration
"""
config: dict = {
    "appName": "Monitor",
    "db": "main.db",
    "gui": {
        "warningTimes": [60*1, 60*3, 60*5]
    },
    "timeLimit": 60*45,
    "bufferSec": 5,
    "keystrokeBufferSec": 5
}
