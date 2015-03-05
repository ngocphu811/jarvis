#!/usr/bin/env python

import os
import sys
import wit
import time
import logging
import GoogleTTS as gtts
import multiprocessing as mp
import socket
import yaml
import glob
import wave  
import misc
import pprint as pp
import json

from zmqclass import *

###################################################################################

class Microphone:

	def __init__(self,wit_token,real,stdin):
		self.real = real
		self.stdin = stdin
		
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('Jarvis')
		
		self.wit_token = wit_token
		wit.init()
	
	def __del__(self):
		#wit.close() # why doesn't this work??
		print 'Microphone closing'
		
	"""
	Will grab audio from microphone or text from keyboard and process the wit.ai json message
	in: nothing
	out: dict {intent, [entities]}
	"""
	def stt(self):
		txt = dict()
		result = ''
		ret = False
		
		if self.real:
			result = wit.voice_query_auto( self.wit_token )
			ans = self.getKey( json.loads(result) )
			
			if ans['intent'] == 'attention':
				self.logger.info('[*] Listening')	
				self.playSound('../sounds/misc/beep_hi.wav')
				result = wit.voice_query_auto( self.wit_token )
				self.logger.info('[*] Done listening')
				self.playSound('../sounds/misc/beep_lo.wav')
				ret = True
			else:
				self.logger.info('[-] Error, no audio detected')	
				ret = False
		else:
			print 'You:'
			result = self.stdin.readline()
			result = wit.text_query(result, self.wit_token )
			ret = True
		
		txt = self.getKey( json.loads(result) )
		if txt['intent'] == 'error':
			ret = False
			
		return txt, ret
	
	def playSound(self, snd):
		os.system('afplay %s'%(snd))

	"""
	Gets intent from msg and handles errors
	in: wit.ai message
	out: dict {intent, [entities]}
	"""
	def getKey(self,msg):
		pp.pprint( msg )
		
		key = 'error'
		ent = []
		
		print type(msg)
	
		# hangle errors ----------------------------
		if not msg:
			self.logger.debug('<< no msg >>')
			key = 'error'
		elif 'outcomes' not in msg:
			self.logger.debug('no outcome')
			key = 'error'
		elif msg['outcomes'][0]['intent']: # assume [0] is highest outcome for now FIXME: 4 mar 15
			key = msg['outcomes'][0]['intent']
			ent = msg['outcomes'][0]['entities']
		
		ans = dict()
		ans['intent'] = key
		ans['entities'] = ent
		
		return ans 

	
	

####################################################################
# 
# 
####################################################################
class SoundServer(mp.Process):
	def __init__(self,YAML_FILE,REAL,stdin=os.fdopen(os.dup(sys.stdin.fileno())),host="localhost",port=9200):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		self.tts = gtts.GoogleTTS()
		
		# publisher
		self.pub = Pub()
		
		#self.getKeys()
		self.info = self.readYaml(YAML_FILE)
		
		# setup WIT.ai
		wit_token = self.info['WIT_TOKEN']
		
		if wit_token is None:
			self.logger.info( 'Need Wit.ai token, exiting now ...' )
			exit()	
		else:
			self.logger.info('Wit.ai API token %s'%(wit_token))
		
		# get microphone	
		use_mic = REAL
		self.mic = Microphone(wit_token,use_mic,stdin)
		
		# Grab plugins
		path = "../plugins/"
		self.modules = []
		#modules = {}
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module':
				mod = __import__(fname)
				m=mod.Plugin()
				# not sure how to handle random with multiple intents??
				#modules[m.intent] = m
				#for i in m.intent:
				#	modules[i] = m
				self.modules.append( m )
		sys.path.pop(0)
		#print modules
	
	"""
	Read a yaml file and return the corresponding dictionary
	todo: duplicate of what is already in Module
	in: file name
	out: dict
	"""
	def readYaml(self,fname):
		f = open( fname )
		dict = yaml.safe_load(f)
		f.close()
		
		return dict
	
	"""
	Converts text to speech using tools in the OS FIXME: select Linux/OSX
	in: text
	out: None
	"""
	def playTxt(self,txt):
		if True:
			fname = self.tts.tts(txt)
			os.system('afplay %s'%(fname))
		else:
			os.system('say -v vicki ' + txt)
	
	"""
	Main process run loop
	in: none
	out: none
	"""
	def run(self):
		# main loop
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ 
			str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		run = True
		while run:		
			print 'loop'	
			# get wit.ai json 
			result,ret = self.mic.stt()
			if ret:
 				# handle dynamic responses ------------------
				for m in self.modules:
					if m.handleIntent( result['intent'] ):
						print result
						txt = m.process( result['entities'] )
				
				if txt == 'exit_loop':
					run = False
				elif txt == 'empty':
					pass
				elif txt != '':
					self.logger.debug('response'+txt)
					self.playTxt(txt)
		
		self.playTxt('Good bye ...')



if __name__ == '__main__':
	#output_file = StringIO()
	s = SoundServer('/Users/kevin/Dropbox/accounts.yaml', True)
	s.run()
	print 'bye ...'
	