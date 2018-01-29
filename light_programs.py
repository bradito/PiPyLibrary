import time
from neopixel import Adafruit_NeoPixel, Color, ws
import argparse
import signal
import sys
import RPi.GPIO as GPIO
from random import random, randrange
from colorsys import hsv_to_rgb


#TODO create a class for my strip
#has a list of its own programs - Dictonary of the programs.
#have a config file for LED strip details?
#create a thread and event



def signal_handler(signal, frame):
		colorWipe(strip, Color(0,0,0))
		sys.exit(0)

def opt_parse():
		parser = argparse.ArgumentParser()
		parser.add_argument('-c', action='store_true', help='clear the display on exit')
		args = parser.parse_args()
		if args.c:
				signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
SWITCH_PIN     = 21	     # GPIO pin for a switch
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

#setup GPIO
GPIO.setmode(GPIO.BCM) #broadcom pin numbering
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


### pattern programs ###
def altColor(strip, colors, wait_ms=20):
	"""alternates colors in the list provided"""
	[strip.setPixelColor(pixel, color) for index,color in enumerate(colors) for pixel in range(strip.numPixels()) if pixel%len(colors) == index]
	strip.show()


#seems to be some error here but not sure what.
def random_blinker(strip, color, duration=10, flash_ms=10, percent_on=0.15):
	"""blinks lights randomly at percent of whole strip to give strobe effect"""
	start = time.time()
	lights_on = []
	max_on = strip.numPixels() * percent_on
	while start + duration > time.time():
		if len(lights_on) < max_on:
			next_on = randrange(strip.numPixels())
			if next_on not in lights_on:
				lights_on.append(next_on)
		else:
			for i in range(strip.numPixels()):
				if i in lights_on:
					strip.setPixelColor(i, color)
				else:
					strip.setPixelColor(i, Color(0,0,0))
			strip.show()
			lights_on = lights_on[1:]
			time.sleep(flash_ms/1000)

def getLightsOn(items):
	count_on = []
	for k, v in items.items():
		if v.get('bright',0) == 0.0:
			count_on.append(k)
	return count_on

#seems to be some error here but not sure what.
def firefly(strip, duration=10, steps_up=3, steps_total=8, step_delay_ms=10, percent_on=0.15):
	"""blinks lights randomly at percent of whole strip 
	but with ramp up/down of randomized light color
	to simulate fireflies"""
	start = time.time()
	lights = {}

	#create simple data structure with dictionary item for each light
	for lite in range(strip.numPixels()):
		lights[lite] = {'hue': 0.0}
		lights[lite] = {'bright':  0.0}
		lights[lite] = {'step' :  -1 }

	max_on = strip.numPixels() * percent_on



	while start + duration > time.time():
		#determine if to seed another light by setting the step 
		current_on = getLightsOn(lights)
		if len(current_on) < max_on:
			next_on = randrange(strip.numPixels())
			if next_on not in current_on:
				lights[next_on]['hue']= random()
				lights[next_on]['bright'] = 0.001
				lights[next_on]['step'] = 0

		#cycle through those needing a step increment
		for key, lite in lights.items():
			if lite['step'] == steps_total:
				lite['bright'] = 0
				lite['step'] = -1

			if (lite['step'] > 0): 
				if (lite['step'] <= steps_up):
					lite['bright'] = lite['step'] / steps_up
				else:
					lite['bright'] = (steps_total - lite['step']) / (steps_total - steps_up)

			print("light on :{} - step:{} - brightness: {}".format(lite,lite['step'],lite['bright']))
			lite['step'] = lite['step'] + 1 

			current_color = hsv_to_rgb(lite['hue'] , 1, lite['bright'])

			current_int_color = Color(
									int(current_color[0]*255),
									int(current_color[1]*255),
									int(current_color[2]*255))  

			strip.setPixelColor(key, current_int_color)

		strip.show()
		time.sleep(step_delay_ms/1000)

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)



# Main program logic follows:
if __name__ == '__main__':
	# Process arguments
	opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT
							, LED_PIN
							, LED_FREQ_HZ
							, LED_DMA
							, LED_INVERT
							, LED_BRIGHTNESS
							, LED_CHANNEL
							, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print ('Press Ctrl-C to quit.')
	try:
		while True:
			if not GPIO.input(SWITCH_PIN): # button is high, and therefore released
				altColor(strip, [Color(0,255,0)])
				time.sleep(1)
			else: # button is pressed
				print ('firefly')
				firefly(strip)
				print ('Random Blinker')
				random_blinker(strip, Color(255, 255, 255))
				print ('Color wipe animations.')
				colorWipe(strip, Color(255, 0, 0))  # Red wipe
				colorWipe(strip, Color(0, 255, 0))  # Blue wipe
				colorWipe(strip, Color(0, 0, 255))  # Green wipe
				print ('Theater chase animations.')
				theaterChase(strip, Color(127, 127, 127))  # White theater chase
				theaterChase(strip, Color(127,   0,   0))  # Red theater chase
				theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
				print ('Rainbow animations.')
				rainbow(strip)
				rainbowCycle(strip)
				theaterChaseRainbow(strip)
	except KeyboardInterrupt: # if ctrl-c pressed
		GPIO.cleanup()