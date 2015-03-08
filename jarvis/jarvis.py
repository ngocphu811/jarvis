#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright Kevin J. Walchko 1 Mar 2015
#------------------
# 1 Mar 2015 Created - ported from my soccer robot

import argparse # command line args

from SoundServer import *

def main(args):
	NAME = args['name']
	KEY_LOC = args['keys']
	MIC = not args['voice']
	s = SoundServer(KEY_LOC, MIC)
	s.run()


def handleArgs():
	parser = argparse.ArgumentParser('A simple helper program')
	parser.add_argument('-n', '--name', help='name of AI, default jarvis', default='jarvis')
	parser.add_argument('-k', '--keys', help='location of API keys', default='/Users/kevin/Dropbox/accounts.yaml')
	parser.add_argument('-v', '--voice', help='Disable voice recognition, default to text input', default=False)
	parser.add_argument('-f', '--video', help='Disable face recognition', default=True)
	parser.add_argument('-c', '--camera', help='camera device', default=0)
	# network stuff for zmq
	# camera device
	
	args = vars(parser.parse_args())
	return args
	
if __name__ == '__main__':
	args = handleArgs()
	main(args)
	print 'Exiting ... bye'
	
	