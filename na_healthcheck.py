#!/bin/python -u

'''
--------------------------------------------------------------------------------
    Type:           Python 2.x script
    Author:         Milan Toman (milan.v.toman@gmail.com)
    Description:    NetApp healthcheck utility

    TOOD:           

--------------------------------------------------------------------------------
            Import libraries
--------------------------------------------------------------------------------
'''
# mandatory
import requests
import urllib
import json
import sys
import os
import re
import textwrap
import getpass
# getopt or argparse, not sure which to go by
import argparse
#import getopts
import time
import datetime
import logging
# optional
import pprint
import sys
#sys.path.append("<path_to_nmsdk_root>/lib/python/NetApp")
from NaServer import *
'''
--------------------------------------------------------------------------------
            Define variables
--------------------------------------------------------------------------------
'''
_VERSION = 0.5
_NAME = u"NetApp_healthcheck"
_LOG_DIR = u'./log/'
_LOG_FILE = _LOG_DIR + re.sub(u'./', '', sys.argv[0]) + u'.log'
_DEBUG_FILE = _LOG_DIR + re.sub(u'./', '', sys.argv[0]) + u'.dbg'

#disable certificate warnings
requests.packages.urllib3.disable_warnings() 

# Huawei specific
_HOST = ''
_PORT = 443
_USER = u''
_PASS = u''


'''
--------------------------------------------------------------------------------
            Set up logging
--------------------------------------------------------------------------------
'''
# Check log directory and create if non-existent
if os.path.isdir(_LOG_DIR):
    # print "INFO: Log directory \"{}\" exists.".format(_LOG_DIR)
    pass
else:
    try:
        os.mkdir(_LOG_DIR)
        # print "INFO: Created logging directory \"{}\"".format(_LOG_DIR)
    except () as error:
        print u"FATAL: Unable to create " +\
              u"logging directory \"{}\"".format(_LOG_DIR)
        raise SystemError(u"Unable to create log directory %s", error)
        
    
# Check for previous logs and rename if any
if os.path.isfile(_LOG_FILE):
    timestapmp_logfile = os.path.getmtime(_LOG_FILE)
    date_logfile = datetime.datetime.fromtimestamp(timestapmp_logfile)
    _LOG_RENAME = _LOG_FILE + "." + date_logfile.strftime("%Y%m%d%H%M%S")
    os.rename(_LOG_FILE, _LOG_RENAME)
if os.path.isfile(_DEBUG_FILE):
    timestapmp_logfile = os.path.getmtime(_DEBUG_FILE)
    date_logfile = datetime.datetime.fromtimestamp(timestapmp_logfile)
    _DEBUG_RENAME = _DEBUG_FILE + "." + date_logfile.strftime("%Y%m%d%H%M%S")
    os.rename(_DEBUG_FILE, _DEBUG_RENAME)

# Cleanup if more than _MAX_LOGS / _MAX_LOGS_SIZE logs are present
    # TODO
    
# Setup formatting
_basic_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
_basic_formatter = logging.Formatter(_basic_format)
_debug_format = "%(asctime)s %(name)s[%(process)d] \
                 (%(funcName)s) %(levelname)s %(message)s"
_debug_formatter = logging.Formatter(_debug_format)
_console_format = "%(name)s %(levelname)s: %(message)s"
_console_formatter = logging.Formatter(_console_format)

# Make logging readable with module hierarchy
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Setting up handlers for stdout / file logging and debug
# Logfile
basic_handler = logging.FileHandler(_LOG_FILE)
basic_handler.setLevel(logging.ERROR)
basic_handler.setFormatter(_basic_formatter)
logger.addHandler(basic_handler)

# Debug file
debug_handler = logging.FileHandler(_DEBUG_FILE)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(_debug_formatter)
logger.addHandler(debug_handler)

# Console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL)
console_handler.setFormatter(_console_formatter)
logger.addHandler(console_handler)

# Just for debugging
# print _LOG_FILE, _DEBUG_FILE
# logger.debug(u'debug message')
# logger.info(u'info message')
# logger.warn(u'warn message')
# logger.error(u'error message')
# logger.critical(u'critical message')


'''
--------------------------------------------------------------------------------
            Setup arguments and Options
--------------------------------------------------------------------------------
'''
desc = u'''\
DESCRIPTION:
    NetApp ONTAP 9.1 healthcheck utility. C-Mode
    '''
epi = u'''\
    ERROR CODES:
         1: 
         
    EXAMPLES:
    
    '''
formatter = argparse.RawDescriptionHelpFormatter
arg_parser = argparse.ArgumentParser(description = desc, 
                                     formatter_class = formatter,
                                     epilog = textwrap.dedent(epi))
ip_help = u'IP or FQDN of the NetApp storage box'
user_help = u'Username, obviously'
password_help = u'Optionally, the password may be supplied'
arg_parser.add_argument('-i', '--ip',
                        type = str, 
                        help = ip_help)
arg_parser.add_argument('-u', '--user',
                        type = str, 
                        help = user_help)
arg_parser.add_argument('-p', '--password',
                        type = str,
                        help = password_help)
args = arg_parser.parse_args()
_HOST = args.ip
                   

'''
--------------------------------------------------------------------------------
            Generic, standalone functions
--------------------------------------------------------------------------------
'''         
def printline():
    line = ''
    for i in range(0, 79):
        line = line + '-'
    print line
    
def print_stuff(content, **kwargs):
    if 'iter' in kwargs.keys():
        iteration = kwargs['iter']
    else:
        iteration = 0
    pause = u''
    for i in range(0, iteration):
        try:
            pause = pause + '  '
        except:
            pause = '  '
    if type(content) is type(dict()):
        for element in content.keys():
            print "{}[ {} ]".format(pause, element)
            print_stuff(content[element], iter = iteration + 1)
    elif type(content) is type(list()):
        for element in content:
            print_stuff(element, iter = iteration + 1)
    elif type(content) is type(str()) or type(int()):
            print "{} -> \"{}\"".format(pause, content)
 
        
    

'''
--------------------------------------------------------------------------------
            Classes
--------------------------------------------------------------------------------
'''







'''
--------------------------------------------------------------------------------
            Main
--------------------------------------------------------------------------------
'''
if '__main__':
    #pass
    