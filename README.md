# Jarvis

A simple Jarvis written in Python.

## Libraries Used

You need the following key python libraries installed:

* python-forecastio - weather
* PyWit - text-to-speech
* twilio - SMS
* PyAudio - recording sound (had to build from scratch)
* PyYAML - read yaml config files
* zmq - network connections

## Sound Server

Jarvis uses [wit.ai](https://wit.ai) to understand the spoken word, turning speech in to text (stt). There are a bunch of plugins which act upon the text to perform different things:

 * Say current time
 * Say current date
 * Send a text message using [Twilio](https://www.twilio.com)
 * Tell a joke (most of the jokes are not funny)
 * Say a greeting
 * Tell you to stop being mean or cursing
 * Play random sound bites from movie and tv shows:
 	* Venture Brothers
 	* Blues Brothers
 	* Star Wars
 * Tell current or future weather forecast using [Forcast.io](http://forecast.io)
 * Grab news headlines
 * General help info
 
Additionally, the text-to-speech part uses [Google Translate](https://translate.google.com) (which sounds the best) or uses `say`.

## To Do's

* There is still a lot to do