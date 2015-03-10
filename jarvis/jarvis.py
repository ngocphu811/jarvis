#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright Kevin J. Walchko 1 Mar 2015
#------------------
# 1 Mar 2015 Created - ported from my soccer robot

import argparse # command line args

from SoundServer import *
from CameraServer import *

JARVIS_VER = '0.0.1'

hello = """
**********************************
* \t%s %s
**********************************
"""


def main(args):
	NAME = 'jarvis' # args['name']
	KEY_LOC = args['keys']
	MIC = args['voice']
	VIDEO = args['video']

	print hello%(NAME,JARVIS_VER)

	try:
		s = SoundServer(KEY_LOC, MIC)
		s.start()

		#if VIDEO v = CameraServer()

		s.join()

	except Exception, e:
			logger.error('Error: ', exc_info=True)

# args: keys audio camera number verbose
#
def handleArgs():
	parser = argparse.ArgumentParser('A simple helper program')
	#parser.add_argument('-n', '--name', help='name of AI, default jarvis', default='jarvis')
	parser.add_argument('-k', '--keys', help='location of API keys', default='/Users/kevin/Dropbox/accounts.yaml')
	parser.add_argument('-a', '--audio', help='Enable voice recognition, default to text input', default=True)
	parser.add_argument('-c', '--camera', help='Enable face recognition', type=bool, default=False)
	parser.add_argument('-n', '--number', help='camera device', type=int, default=0)
	parser.add_argument('-v', '--verbose', help='increase the verbosity', action='count')
	# network stuff for zmq
	# camera device

	args = vars(parser.parse_args())
	if args.verbose:
			print ' you want verbose output ... i should do something then :)'

	return args

if __name__ == '__main__':
	args = handleArgs()
	main(args)
	print 'Exiting ... bye'
