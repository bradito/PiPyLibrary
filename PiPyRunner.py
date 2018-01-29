# libraryFlask.py
from flask import Flask, render_template
from astral import Astral
import datetime
import light_programs

#create object of our strip
#create thread event and laucncher

app = Flask(__name__)

@app.route("/")
def homepage():
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")
	#Add a list of programs to display
	return render_template('main.html', **templateData)


@app.route('/update/<action>')
def update(action):
	"""set a new program from the letter in the URL"""
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")
	return render_template('main.html', **templateData)


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
	app.run(host='0.0.0.0', port=80, debug=False)



