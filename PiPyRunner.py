# libraryFlask.py
from flask import Flask, render_template
from astral import Astral
import datetime
import threading
import time

#
#create object of our strip
#create thread event and laucncher

stopEvent = threading.Event()
lightsThread = None


def printoften(e):
	while not e.isSet():
		now = datetime.datetime.now()
		timestring = now.strftime("%Y-%m-%d %H:%M")
		print('The current time', timestring)
		time.sleep(4)

app = Flask(__name__)

@app.route("/")
def homepage():
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")
	#Add a list of programs to display
	return render_template('main.html', timestring=timestring, message = "")


@app.route('/update/<action>')
def update(action):
	"""set a new program from the letter in the URL"""
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")
	return render_template('main.html', timestring=timestring, message = "")

@app.route('/start')
def startpage():
	global stopEvent
	global lightsThread
	t1 = threading.Thread(target=printoften,
						  args=(stopEvent,))
	t1.start()
	print("started")
	lightsThread = t1
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")
	return render_template('main.html', timestring=timestring, message = ("thread started:",t1))

@app.route('/stop')
def stoppage():
	global stopEvent
	global lightsThread
	stopEvent.set()
	print("stopping soon")
	lightsThread.join()

	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")
	
	stopEvent.clear()
	return render_template('main.html', timestring=timestring, message = ("thread stopped:",lightsThread))


@app.context_processor
def utility_processor():
    def format_hex(r,g,b):
        return u'{:02x}{:02x}{:02x}'.format(r,g,b)
    return dict(format_hex=format_hex)

@app.route("/sunset")
def sunset():
	city_name = 'Minneapolis'
	a = Astral()
	a.solar_depression = 'civil'

	city = a[city_name]
	sun = city.sun(date=datetime.datetime.now(), local=True)

	return 'Sunset for {}: {}'.format(city_name, sun['sunset'])


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=False)



