# The MIT License (MIT)

# Copyright (c) 2016 Nicholas E. Johnson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
import serial
from datetime import datetime

__author__ = "Nicholas E. Johnson <nejohnson2@gmail.com>"
__copyright__ = "Copyright (C) 2016 Nicholas Johnson"
__license__ = "MIT"
__version__ = "v1.0"

class Dylos(object):
	"""docstring for Dylos"""
	def __init__(self, port):
		self.port = port
		try:
			self.ser = serial.Serial(port=self.port 
							, baudrate=9600
							, parity=serial.PARITY_NONE
							, stopbits=serial.STOPBITS_ONE
							, bytesize=serial.EIGHTBITS)
		except IOError as e:
			print "Serial connection failed\n%s" %(e)
			raise

		self.ser.flushInput()
		self.ser.flushOutput()
		time.sleep(0.1)			

	def write_csv(self, results):
		'''Write data to a csv file'''
		fname = './capture.csv'

		with open(fname, 'a') as f:
			w = csv.DictWriter(f, results.keys())
			w.writerow(results)

		f.close()

	def read(self, store=False):
		"""Read serial data in non-blocking

		Parameters:
		----------
		store: boolean,
			Set true to write to csv file
		"""			
		print "Listening for Dylos data..."
		while True:
			# read serial port until '\n'
			data = self.ser.readline().rstrip().split(",")

			# calculate 0.5-2.5um 
			fine_pm = int(data[0]) - int(data[1])
			greater_pm2_5 = int(data[1])

			# create dict with captured data and timestamp
			counts = {
				'time' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
				'fine'	: fine_pm,
				'small' : data[0], # >0.5um
				'large' : data[1] # >2.5um				
			}
			print counts

			if store:
				self.write_csv(counts)

		self.ser.close()		

	def __del__(self):
		'''Cleanup'''
		try:
			self.ser.close()
			print "Closed serial port"
		except:
			pass
		print "Cleaning up Dylos class"	


if __name__ == '__main__':
	port = '/dev/ttyUSB0'

	try:
		d = Dylos(port)
	except:
		print "Unable to setup serial communication"
		sys.exit()
	# runs forever
	d.read()

	sys.exit()