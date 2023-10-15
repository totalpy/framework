import TotalPy.utils
import TotalPy.http
import TotalPy.nosql
import TotalPy.flow
import TotalPy.tangular
import TotalPy.edit
import TotalPy.mail
import TotalPy.builders
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
import importlib.util

directory = sys.path[0]
ready = False

# Configuration
config = {
	'name': 'Total.py',
	'version': '1'
}

print('JEEBBO')

# Resources
resources = {}

# Internal cache
cache = {}

internal = {
	'controllers': {},
	'modules': {},
	'plugins': {},
	'schemas': {},
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

class Dependency():
	pass

def inject(filename):
	tmp = {}
	content = open(filename).read()
	exec(content, globals(), tmp)
	return tmp

def load(types = None):

	# Load configuration
	# Load directories
	# Load HTTP

	try:
		file = open('config', 'r')
		cfg = utils.parseconfig(file.read())
		for key in cfg:
			config[key] = cfg[key]
	except:
		pass

	install = []

	dir = TotalPy.path.modules()
	if os.path.isdir(dir):
		for file in os.listdir(dir):
			name = file.replace('.py', '')
			tmp = inject(TotalPy.path.join(dir, file))
			internal['modules'][name] = tmp
			install.append(tmp)

	dir = TotalPy.path.controllers()
	if os.path.isdir(dir):
		for file in os.listdir(dir):
			name = file.replace('.py', '')
			tmp = inject(TotalPy.path.join(dir, file))
			internal['controllers'][name] = tmp
			install.append(tmp)


	dir = TotalPy.path.schemas()
	if os.path.isdir(dir):
		for file in os.listdir(dir):
			name = file.replace('.py', '')
			tmp = inject(TotalPy.path.join(dir, file))
			internal['schemas'][name] = tmp

	dir = TotalPy.path.plugins()
	if os.path.isdir(dir):
		for item in os.listdir(dir):

			filename = TotalPy.path.join(TotalPy.path.join(dir, item), 'index.py')
			isindex = os.path.isfile(filename)
			if isindex == False:
				continue

			tmp = inject(filename)
			internal['plugins'][dir] = tmp
			install.append(tmp)

			for dependency in ('definitions', 'schemas'):
				subdir = TotalPy.path.join(dir, dependency)
				if os.path.isdir(subdir):
					for f in os.listdir(subdir):
						inject(TotalPy.path.join(subdir, f))

	for step in os.walk(TotalPy.path.definitions()):
		for file in step[2]:
			inject(TotalPy.path.join(step[0], file))

	for mod in install:
		if 'install' in mod:
			print(mod.get('install')())

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

def auth(callback = None):
	if callback == None:
		def action(func):
			delegates['auth'] = func
	else:
		delegates['auth'] = callback

def localize(callback = None):
	if callback == None:
		def action(func):
			delegates['localize'] = func
	else:
		delegates['localize'] = callback

def route(url, action = None):

	# decorator
	if action == None and url.find('*') == -1:
		def action(func):

			r = TotalPy.routing.Route(url, func)

			if r.append == True:
				routes['web'].append(r)

			if ready:
				TotalPy.routing.sort()

		return action

	r = TotalPy.routing.Route(url, action)

	if r.append == True:
		routes['web'].append(r)

	if ready:
		TotalPy.routing.sort()

endpoint = route

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
