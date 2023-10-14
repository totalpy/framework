# HTTP Server

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

import TotalPy
import time as ts
import json
import re

REG_MOBILE = re.compile('Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet', re.IGNORECASE)
REG_ROBOT = re.compile('search|agent|bot|crawler|spider', re.IGNORECASE)

class Listener(BaseHTTPRequestHandler):

	def log_message(self, format, *args):
		pass

	def do_GET(self):
		ctrl = Controller(self, 'GET')
		if ctrl.uri['file'] == False:
			ctrl.init()
			ctrl.evaluate()
		else:
			ctrl.throw(404)

	def do_POST(self):
		ctrl = Controller(self, 'POST')
		if ctrl.uri['file'] == False:
			ctrl.init()
			ctrl.evaluate()
		else:
			ctrl.throw(404)

	def do_PUT(self):
		ctrl = Controller(self, 'PUT')
		if ctrl.uri['file'] == False:
			ctrl.init()
			ctrl.evaluate()
		else:
			ctrl.throw(404)

	def do_PATCH(self):
		ctrl = Controller(self, 'PATCH')
		if ctrl.uri['file'] == False:
			ctrl.init()
			ctrl.evaluate()
		else:
			ctrl.throw(404)

	def do_DELETE(self):
		ctrl = Controller(self, 'DELETE')
		if ctrl.uri['file'] == False:
			ctrl.init()
			ctrl.evaluate()
		else:
			ctrl.throw(404)

def run(ip = '0.0.0.0', port = 8000):
	server_address = (ip, port)
	httpd = ThreadingHTTPServer(server_address, Listener)
	print('http://%s:%s' % server_address)
	httpd.serve_forever()

class Controller:

	def __init__(self, req, method):

		self.method = method
		self.req = req
		self.route = None
		self.uri = TotalPy.utils.parseuri(req.path)
		self.url = self.uri['url']
		self.headers = req.headers
		self.split = []
		self.splitcompare = [] # lower case
		self.params = {}

		tmp = self.uri['pathname'].split('/')
		for m in tmp:
			if m != '':
				self.splitcompare.append(m.lower())
				self.split.append(m)

		if self.headers.get('x-requested-with') == 'XMLHttpRequest':
			self.xhr = True
		else:
			self.xhr = False

		ip = self.headers.get('x-forwarded-for')

		if ip != None:
			self.ip = ip
		else:
			self.ip = self.req.client_address[0]

		self.ts = ts.time()
		self.query = self.uri.get('query')
		self.files = []
		self.body = {}
		self.user = None
		self.session = None
		self.internal = {
			'status': 200,
			'headers': {}
		}

	def ip(self):
		ip = self.headers.get('x-forwarded-for')
		if ip == None:
			return self.req.client_address[0]
		return ip

	def ua(self):
		return parseua(self.headers.get('user-agent'))

	def mobile(self):
		return REG_MOBILE.search(self.headers.get('user-agent'))

	def robot(self):
		return REG_ROBOT.search(self.headers.get('user-agent'))

	def init(self):

		auth = TotalPy.delegates.get('auth')

		if auth is None:
			self.user = None
		else:
			self.user = auth(self)

		localize = TotalPy.delegates.get('localize')

		if localize is None:
			self.language = None
		else:
			self.language = localize(self)

	def status(self, code):
		self.internal['status'] = code

	def throw(self, code = 404, error = None):
		self.req.send_response(code)
		self.req.end_headers()

	def throw400(self, error = None):
		self.throw(400, error)

	def throw401(self, error = None):
		self.throw(401, error)

	def throw404(self, error = None):
		self.throw(404, error)

	def throw409(self, error = None):
		self.throw(409, error)

	def throw500(self, error = None):
		self.throw(500, error)

	def success(self, value = None):
		self.json({ 'success': True, 'value': value })

	def json(self, value):
		self.req.send_response(self.internal.get('status'))
		self.req.send_header('Content-type', 'application/json')
		self.req.end_headers()
		self.req.wfile.write(json.dumps(value, separators=(',', ':')).encode('utf8'))

	def html(self, value):
		self.req.send_response(self.internal.get('status'))
		self.req.send_header('Content-type', 'text/html')
		self.req.end_headers()
		self.req.wfile.write(str(value).encode('utf8'))

	def plain(self, value):
		self.req.send_response(self.internal.get('status'))
		self.req.send_header('Content-type', 'text/plain')
		self.req.end_headers()
		self.req.wfile.write(str(value).encode('utf8'))

	def empty(self):
		self.req.send_response(204)
		self.req.end_headers()

	def invalid(self, error):
		self.req.send_response(400)
		self.req.send_header('Content-type', 'application/json')
		self.req.end_headers()
		err = ErrorBuilder(error)
		self.req.wfile.write(json.dumps(err.stringify(self.language), separators=(',', ':')).encode('utf8'))

	def view(self, name, model):
		pass

	def evaluate(self):

		route = TotalPy.routing.lookup(self, None)

		if route != None:

			# Parse params
			self.route = route

			if len(route.params):
				for param in route.params:
					value = self.split[param['index']]
					match param['type']:
						case 'string':
							self.params[param['name']] = value
							break
						case 'uid':
							# TODO: make validation
							self.params[param['name']] = value
							break
						case 'guid':
							# TODO: make validation
							self.params[param['name']] = value
							break
						case 'number':
							# TODO: make validation
							self.params[param['name']] = int(value)
							break
						case 'boolean':
							self.params[param['name']] = value == 'true'
							break
						case 'date':
							# TODO: make validation
							self.params[param['name']] = utils.parsedate(value)
							break

			route.callback(self)
		else:
			self.throw404()