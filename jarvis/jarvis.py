#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright Kevin J. Walchko 1 Mar 2015
#------------------
# 1 Mar 2015 Created - ported from my soccer robot

import argparse # command line args

def main(NAME, KEY_LOC):


def handleArgs():
	parser = argparse.ArgumentParser('A simple helper program')
	parser.add_argument('-n', '--name', help='name of AI, default jarvis', default='jarvis')
	parser.add_argument('-k', '--keys', help='location of API keys', default='/Users/kevin/Dropbox/accounts.yaml')
	# network stuff for zmq
	# camera device
	
	args = vars(parser.parse_args())
	return args
	
if __name__ == '__main__':
	args = handleArgs()
	
	main(args['name'],args['keys'])
	
	