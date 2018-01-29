#a dummy library to allow other to compile

class Adafruit_NeoPixel: 
	def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False):
		self.numberPixels = num

	def begin(self):
		pass

	def getPixelColor(self, n):
		pass
	
	def getPixels(self):
		pass

	def numPixels(self):
		return self.numberPixels
		


	def setBrightness(self, brightness):
		pass

	def setPixelColor(self, n, color):
		print('Pix: {} Color: {}'.format(n, color))
		pass
#     Set LED at position n to the provided 24-bit color value (in RGB order).

	def setPixelColorRGB(self, n, red, green, blue):
		pass
#     Set LED at position n to the provided red, green, and blue color.
#     Each color component should be a value from 0 to 255 (where 0 is the
#     lowest intensity and 255 is the highest intensity).

	def show(self):
		pass


def  Color(red, green, blue):
	pass


#         Convert the provided red, green, blue color to a 24-bit color value.
#         Each color component should be a value 0-255 where 0 is the lowest intensity
#         and 255 is the highest intensity.