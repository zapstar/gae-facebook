import webapp2

#Start of State Variable Class
class SessionStateVariable:
	#Emulates the PHP uniqid() function
	def uniqid(self, prefix = '', more_entropy = False):
		from time import time
		m = time()
		from math import floor
		myuniqid = '%8x%05x' % (floor(m), (m - floor(m))*1000000)
		from string import hexdigits
		if more_entropy:
			valid_chars = list(set(hexdigits.lower()))
			entropy_string = ''
			for i in range(0,10,1):
				from random import choice
				entropy_string += choice(valid_chars)
			myuniqid = myuniqid + entropy_string
		myuniqid = prefix + myuniqid
		return myuniqid

	#Generates state variable as suggested by Facebook
	#in server side OAuth 2.0 flow (PHP Example)
	def generateState(self):
		from random import randint
		from md5 import md5
		#the max value of randint as per a Linux server
		#change it to any needed value.
		return md5(self.uniqid(str(randint(0,2147483647)), True)).hexdigest()
#End of StateVariable Class