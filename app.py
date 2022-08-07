# Raspberry pi weather station v1.0 written by Saahil Thadani (180642E)
'''
 Pins used
 4, 6 - VCC and GND connected to fourdigit led
 3, 5 - SDA, SCL for fourdigit
 1 - GP VCC 3.3v
 11 - input to change clock mode between 12 and 24 hour formats
 13 - input to change clock mode between clock and stopwatch
'''

from flask import Flask, render_template, request, send_from_directory, jsonify
from time import sleep
from datetime import datetime

from TM1637 import FourDigit
from sense_hat import SenseHat
from RPi.GPIO import RPi.GPIO as GPIO

# Globals
displayMode = 12
stopwatchTime = 0
display = None
formatButton = 11
modeButton = 13
startstopButton = 15

# Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(formatButton, GPIO.IN)
GPIO.setup(modeButton, GPIO.IN)
hat = SenseHat()

sunny = ["Sunny"]
stormy = ["Moderate or heavy rain shower", "Torrential rain shower",
          "Moderate or heavy rain shower", "Moderate or heavy freezing rain", "Heavy freezing drizzle"]
rainy = ["Light rain shower", "Light freezing rain", "Moderate rain", "Moderate rain at times",
         "Light rain", "Patchy light rain", "Torrential rain shower", "Heavy rain", "Heavy rain at times"]
lightning = ["Moderate or heavy rain with thunder", "Patchy light rain with thunder",
             "Moderate or heavy rain with thunder", "Patchy light rain with thunder"]
cloudy_partial = ["Cloudy", "Partly cloudy", "Overcast"]
cloudy = ["Freezing drizzle", "Light drizzle", "Patchy light drizzle",
          "Thundery outbreaks possible", "Patchy rain possible"]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("resources", path)


@app.route("/resources/<path:path>")
def resources_dir(path):
    return send_from_directory("resources", path)


@app.route('/api/weather')
def getReadings():
    return jsonify({"temperature": "{:.2f}".format(hat.get_temperature()), "humidity": "{:.2f}".format(hat.get_humidity()), "pressure": "{:.2f}".format(hat.get_pressure())})


@app.route('/api/weathericon')
def get_icon():
    name = request.args["input"]
    output = "resources/"
    if name in sunny:
        output += "Sunny.png"
    elif name in stormy:
        output += "Stormy.png"
    elif name in rainy:
        output += "Rainy.png"
    elif name in lightning:
        output += "Lightning.png"
    elif name in cloudy_partial:
        output += "Cloudy_Partial.png"
    elif name in cloudy:
        output += "Cloudy.png"
    else:
        output += "Unknown.png"
    hat.load_image(output)
    return jsonify({"output": output})

# Clock helper function


def clockSetup():
    display = FourDigit(dio=3, clk=5, lum=7)
    display.setColon(True)


def buttonDetection():
    global displayMode, clockMode
    if(GPIO.input(formatButton)):
        displayMode = 12 if displayMode == 24 else 24
    if(GPIO.input(modeButton)):
        stopwatchTime = 0
        clockMode = "clock" if clockMode != "clock" else "stopwatch"
    sleep(1)


def clock():
    if(displayMode == 12):
        currentTime = datetime.now().strftime("%I%M")
    elif(displayMode == 24):
        currentTime = datetime.now().strftime("%H%M")
    display.show(currentTime)


def stopwatch():
    global stopwatchTime
    stopwatchTime += 1
    display.show(str(stopwatchTime))


@app.route('/api/clock')
def displayLoop():
    global display, displayMode, formatButton, clockMode
    if(clockMode == "clock"):
        clock()
    elif(clockMode == "stopwatch"):
        stopwatch()

    buttonDetection()

    return jsonify({"time": currentTime})


if __name__ == '__main__':
    clockSetup()
    app.run()
