"""
Class to capture data from
the Dylos1700

Nov 2016
by Nicholas Johnson
"""

import sys
import time
import serial
from datetime import datetime

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