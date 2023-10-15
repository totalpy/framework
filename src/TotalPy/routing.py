import TotalPy
import re

REG_PARAMS = re.compile(r'\{.*?\}')
REG_FLAGS = re.compile(r'\s@[a-z]+')
REG_ACTION = re.compile(r'\s.*?$', re.IGNORECASE)
REG_MIDDLEWARE = re.compile(r'\s#[a-z]+')

class Route:

	def __init__(self, url, callback = None):

		index = url.find(' ')

		self.method = url[0:index].upper()
		self.auth = 0

		auth = self.method[0]

		if auth == '+':
			self.auth = 1 #authorized
			self.method = self.method[1:].strip()
		elif auth == '-':
			self.auth = 2 #unauthorized
			self.method = self.method[1:].strip()

		self.wildcard = False
		self.api = False
		self.action = None
		self.callback = callback
		self.call = '';

		if self.method == 'API':
			self.api = True
			self.method = 'POST'

		# #middleware
		# @flag

		url = url[index + 1:].strip()

		index = url.find(' *')
		if index != -1:
			self.call = ' '.join(url[index + 1:].strip().split())
			url = url[0:index].strip()

		index = url.find(' ')
		if index == -1:
			index = len(url)
		else:
			action = REG_ACTION.search(url[index:])
			if action != None:
				self.action = re.sub(r'\{|\}|\+', '', re.sub(r'\s{2,}', ' ', action[0])).strip().split('-->')
				self.action = [str.strip() for str in self.action]

		endpoint = url[:index].strip()

		if endpoint.find('*') != -1 or endpoint.find('...') != -1:
			endpoint = endpoint.replace('*', '').replace('...', '')
			self.wildcard = True

		path = endpoint.lower()

		if path == '/':
			self.url = ['/']
		else:
			tmp = path.split('/')
			self.url = []
			for m in tmp:
				if m != '':
					self.url.append(m)

		self.xhr = False
		self.robot = False
		self.mobile = False
		self.upload = False
		self.json = False
		self.xml = False
		self.referer = False
		self.websocket = False
		self.priority = 0
		self.split = split(endpoint)
		self.params = []
		self.append = True

		if self.call != '':
			self.callback = apihandler

		if self.api:
			if TotalPy.internal['routes']['api'].get(endpoint) == None:
				TotalPy.internal['routes']['api'][endpoint] = {}
			else:
				self.append = False

			#if TotalPy.internal['routes']['api'][endpoint].get()
			TotalPy.internal['routes']['api'][endpoint][self.action[0]] = self

		for i in range(0, len(self.split)):
			m = self.split[i]
			if m[0] != '{':
				continue

			keytype = m[1:len(m) - 1].strip().split(':')
			type = 'string'

			if len(keytype) == 2:
				type = keytype[1].strip().lower()

			name = keytype[0].strip()
			self.params.append({ 'name': name, 'type': type, 'index': i })

	def compare(self, ctrl):
		for i in range(0, len(self.url)):
			p = self.url[i]
			if p[0] == '{':
				continue
			if p != ctrl.splitcompare[i]:
				return False
		return True

def compare(ctrl, routes, auth = None):

	status = 0

	for route in routes:

		if auth != None and route.auth != None and route.auth != auth:
			status = 1
			continue

		if route.referer == True and (ctrl.headers.get('referer') == None or ctrl.headers.get('referer').find(ctrl.headers.get('host')) == -1):
			continue

		if route.websocket == False:
			if route.json == True and ctrl.headers.get('content-type') != 'application/json':
				continue
			elif route.xml == True and ctrl.headers.get('content-type') != 'text/xml':
				continue
			if route.xhr == True and ctrl.xhr == False:
				continue
			if route.upload == True and ctrl.headers.get('content-type').find('multipart/form-data') == -1:
				continue

		if route.mobile == True and ctrl.mobile() == False:
			continue

		if route.robot == True and ctrl.robot() == False:
			continue

		return route

	return status

def lookup(ctrl, auth, skip = False):

	key = ctrl.method
	tmp = TotalPy.internal['routes']['web'].get(key)

	if tmp == None:
		return None

	arr = ctrl.split
	url = ctrl.uri['pathname'][1:len(ctrl.uri['pathname']) - 1].lower()

	if url == '':
		url = '/'

	length = len(ctrl.split)
	routes = tmp.get(url)
	route = None

	if routes != None:
		if skip == True:
			return routes[0]
		route = compare(ctrl, routes, auth)
		if route != 0 and route != 1:
			return route;
		routes = None;

	if tmp.get('D') and (length == 1 and arr[0] == '/') == False:
		for r in tmp['D']:
			if len(r.url) == length or r.wildcard == True:
				if r.compare(ctrl):
					if routes == None:
						routes = []
					if skip == True:
						return r
					routes.append(r)
		if routes != None:
			if skip == True:
				return routes[0]
			route = compare(ctrl, routes, auth)
			if route:
				return route

		routes = None

	routes = [];

	for i in range(0, length):
		url = '/'.join(ctrl.split[0:length - i]) + '/*'
		items = tmp.get(url)
		if items != None:
			if skip:
				return items[0]
			for m in items:
				routes.append(m)

	items = tmp.get('/*');
	if items:
		if skip == True:
			return items[0]
		for m in items:
			routes.append(m)

	if routes != None and len(routes) > 0:
		return compare(ctrl, routes, auth)
	else:
		return route

def sort():

	cache = {}

	for route in TotalPy.routes['web']:
		key = route.method
		tmp = cache.get(key)
		if tmp == None:
			tmp = cache[key] = {}

		arr = [];

		for path in route.url:
			arr.append(REG_PARAMS.sub(path, '{}'))

		if route.wildcard == True:
			arr.append('*')

		subkey = '/'.join(arr)

		if subkey.find('{') != -1:
			subkey = 'D'

		if tmp.get(subkey) == None:
			tmp[subkey] = [route]
		else:
			tmp[subkey].append(route)

	TotalPy.internal['routes']['web'] = cache

def split(url, lowercase = True):

	if lowercase == True:
		url = url.lower()

	if url[0] == '/':
		url = url[1:]

	if url != '' and url[len(url) - 1] == '/':
		url = url[:len(url) - 1]

	count = 0
	end = 0
	arr = []

	for i in range(0, len(url)):
		match url[i]:
			case '/':
				if count != 0:
					break
				plus = 0
				if len(arr) > 0:
					plus = 1
				beg = end + plus
				arr.append(url[beg:i])
				end = i
				break

			case '{':
				++count
				break

			case '}':
				--count
				break

	if count == 0:
		plus = 0
		if len(arr) > 0:
			plus = 1
		beg = end + plus
		arr.append(url[beg:len(url)])

	if len(arr) == 1 and arr[0] == '':
		arr[0] = '/'

	return arr

def apihandler(ctrl):

	route = ctrl.route
	action = route.action
	call = route.call


	print(action, call)

	ctrl.success()
	pass
