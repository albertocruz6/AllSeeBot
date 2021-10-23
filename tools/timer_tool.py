from threading import Thread
from time import *

class Timer():

	def __init__(self, seconds):
		self.time_to_wait = seconds

	def run(self):

		def looper():
			for i in range(self.time_to_wait):
				self.time_to_wait -= 1
				sleep(1)
			print("Timer stopped!")
		
		self.countdown_looper = Thread(target = looper)
		self.countdown_looper.start()




# Example of timer to use 
if __name__ == "__main__":
	timer = Timer(10)
	timer.run()
	while timer.time_to_wait > 0:
		print("Loop is on")
		sleep(1)
