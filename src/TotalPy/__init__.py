import TotalPy.utils
import TotalPy.http
import TotalPy.nosql
import TotalPy.flow
import TotalPy.viewengine
import TotalPy.tangular
import TotalPy.edit
import TotalPy.mail
import TotalPy.builders
import TotalPy.internal
import TotalPy.filestorage
import TotalPy.path
import TotalPy.querybuilder
import TotalPy.routing
import TotalPy.jsonschema
import os
import datetime
import math
import sys
import threading

directory = os.path.dirname(sys.path[0])

ready = False

# Configuration
config = {
	'name': 'Total.py',
	'version': '1'
}

# Resources
resources = {}

# Internal cache
cache = {}

internal = {
	'uid': {
		'id': utils.random_text(1),
		'index': 0
	},
	'calls': {},
	'service': 0,
	'routes': {
		'web': {},
		'websockets': {},
		'files': {},
		'api': {}
	}
}

# Temporary cache
temp = {}
main = {}
repo = {}
TEMP = {}

# Events
events = {}

# Delegates
delegates = {}

# Schemas
schemas = {}

# Actions
actions = {}

# Views
views = {}

# Routes
routes = {
	'web': [],
	'file': [],
	'socket': []
}

# Internal stats
stats = {}

# Internal service
def service():
	TotalPy.NOW = datetime.datetime.now()
	index = internal['service']

	if index != 0:
		TotalPy.emit('service', index)
		if index % 5 == 0:
			TEMP.clear()

	internal['service'] = index + 1
	threading.Timer(60, service).start()

def load(types = None):

	# Load configuration
	# Load directories
	# Load server

	try:
		file = open('config', 'r')
		cfg = utils.parseconfig(file.read())
		for key in cfg:
			config[key] = cfg[key]
	except:
		pass

	service()
	routing.sort()
	ready = True

	# Blockes thread
	http.run(config.get('ip') or '0.0.0.0', config.get('port') or 8000)

def loadconfig(data):
	print('loadconfig')

def reconfigure():
	print('reconfigure')

def loadresource(name, data):
	print('loadresource', name, data)

def auth(callback):
	delegates['auth'] = callback

def localize(callback):
	delegates['localize'] = callback

def route(url, action = None):

	r = TotalPy.routing.Route(url, action)

	if r.append == True:
		routes['web'].append(r)

	if ready:
		TotalPy.routing.sort()

def schema(name, declaration):
	print('schema')

# Unique identifier generator
def uid():

	ts = math.floor(datetime.datetime.now().timestamp() * 10)
	h = utils.int2str(ts, 62);
	index = ++internal['uid']['index'];
	plus = '0'

	if (index % 2 == 1):
		plus = '1'

	return str(h) + utils.int2str(index + 99, 62) + internal['uid']['id'] + str(len(h)) + plus + 'f'

def translate(language, text):

	index = text.find('@(')
	length = len(text)

	count = 0

	while index != -1:

		found = False

		for i in range(index + 2, length):
			c = text[i]

			if c == '(':
				++count
				continue

			if c == ')':
				if count > 0:
					--count
					continue
				index = i
				found = True
				break

		if found:
			# replace
			pass

		index = index + 2
		index = text.find('@(', index)

def call(name, model):
	pass

def on(name, callback):

	arr = events.get(name)
	if arr == None:
		arr = []
		events[name] = arr

	arr.append(callback)

def off(name, callback = None):
	arr = events.get(name)
	if arr != None:
		if callback != None:
			arr.remove(callback)
		else:
			del events[name]

# def emit(name, a = None, b = None, c = None, d = None, e = None):
def emit(name, *argv):
	arr = events.get(name)
	if (arr != None):
		for fn in arr:
			fn(*argv)
