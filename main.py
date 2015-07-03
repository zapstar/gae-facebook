#Import WebApp2 framework on Google App Engine
import webapp2

#Import Sessions from WebApp2 Extras
from webapp2_extras import sessions

#Import Quote Function from URL Library
from urllib import quote

#Import Parse_QueryString from URL Parse
from urlparse import parse_qs

#Import URLFetch from Google App Engine API
from google.appengine.api import urlfetch

#Import JSON Loads from JSON
from json import loads

#Import the Session State Variable Generator
#Random String of 23 characters, unguessable
import state_variable

#Import the BaseSessionHandler Class
import session_module

class MainHandler(session_module.BaseSessionHandler):
	#The APP_ID and the APP_SECRET variables contain information
	#required for Facebook Authentication
	APP_ID = '267910489968296'
	APP_SECRET = '02583f888c364e2d54fc081830c8f870'
	
	#If Offline then use this
	#my_url = 'http://localhost:8080/'
	#else if one Google App Engine use this as my_url
	my_url = 'http://facebook-gae-python.appspot.com/'

	def get(self):
		#Check whether 'code' is in the GET variables of the URL
		#if not then execute the below code to set the state variable in
		#the session
		if self.request.get('code') == '':
			#If not generate a state variable
			session_state = state_variable.SessionStateVariable()
			#Set the state variable in the session
			self.session['state'] = session_state.generateState()
			#The Dialog URL for Facebook Login
			dialog_url = 'http://www.facebook.com/dialog/oauth?client_id=' + \
				self.APP_ID + '&redirect_uri=' + quote(self.my_url) + \
				'&state=' + self.session.get('state')
			#Redirect to the Facebook Page (Please note the Redirection URL must
			#be updated on Facebook App's Site URL or Canvas URL
			self.redirect(dialog_url)
		else:
			#If state variable is already set then set the class variable
			self.state = self.session.get('state')
		
		#Check whether the State Variable is same as that returned by Facebook
		#Else report the CSRF Violation
		if self.request.get('state') == self.session.get('state'):
		
			#The token URL for generation of OAuth Access Token for Graph API 
			#Requests from your application
			token_url = 'https://graph.facebook.com/oauth/access_token?client_id=' + \
				self.APP_ID + '&redirect_uri=' + quote(self.my_url) + \
				'&client_secret=' + self.APP_SECRET + '&code=' + self.request.get('code')
			
			#Get the token from the Token URL
			token_response = urlfetch.fetch(token_url)
			
			#Parse the string to get the Access token
			params = parse_qs(token_response.content)
			
			#Now params['access_token'][0] has the access_token for use
			
			#Requesting Facebook Graph API
			#the Graph URL
			graph_url = u'https://graph.facebook.com'
			#The API String for example /me or /me/movies etc.
			api_string = u'/me'
			#The concatenated URL for Graph API Request
			api_request_url = graph_url + api_string + u'?access_token=' + params['access_token'][0]
			#Fetch the Response from Graph API Request
			api_response = urlfetch.fetch(api_request_url)
			#Get the contents of the Response
			json_response = api_response.content
			#Convert the JSON String into a dictionary
			api_answer = loads(json_response)
			#Print your name on the screen!
			self.response.out.write('Hello ' + api_answer['name'])
		else:
			#CSRF Violation Response (if the state variables don't match)
			self.response.out.write('The states dont match. You may a victim of CSRF')
#End of MainHandler Class

#The WebApp2 WSGI Application definition
app = webapp2.WSGIApplication([('/', MainHandler)], debug=True, config = session_module.session_config)