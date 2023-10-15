# Builders

import TotalPy

class Response:
	def __init__(self):
		self.errors = []
		self.replaces = []
		self.response = None
		self.iserr = False

	def replace(self, find, text):
		self.replaces.append({ 'find': find, 'text': text })

	def push(self, error, index = None, path = None):

		if self.iserr == False:
			self.iserr = True

		self.errors.append({ 'error': error })

	def stringify(self, language = ''):

		if self.iserr == False:
			return self.response

		obj = [];

		for m in self.errors:
			# localize errors
			if len(self.replaces) > 0:
				for r in self.replaces:
					m['error'] = m['error'].replace(r['find'], r['text'])
			obj.append(m)

		return obj

class CallerOptions:

	def __init__(self):
		self.name = ''
		self.model = None
		self.query = None
		self.params = None
		self.controller = None
		self.user = None
		self.repo = None

	def ip(self):
		if self.controller == None:
			return None
		else:
			return self.controller.ip()

	def ua(self):
		if self.controller == None:
			return None
		else:
			return self.controller.ua()

class Caller:

	def __init__(self, model = None):
		self.meta = {}
		self.meta.params = None
		self.meta.user = None
		self.meta.query = None
		self.meta.model = None
		self.meta.session = None
		self.meta.controller = None
		self.response = ErrorBuilder()

	def user(self, value):
		self.meta.user = value

	def session(self, value):
		self.meta.session = value

	def query(self, value):
		self.meta.query = value

	def params(self, value):
		self.meta.params = value

	def controller(self, value):
		self.meta.params = value.params
		self.meta.user = value.user
		self.meta.query = value.query
		self.meta.model = value.body
		self.meta.session = value.session
		self.meta.controller = value

	def run(self, name, model = None, controller = None):

		self.name = name

		if controller != None:
			self.controller(controller)

		if model != None:
			self.model = model

		operations = TotalPy.internal['calls'].get(name)

		if operations == None:
			operations = parse(self)

		opt = CallerOptions()

		for action in operations:

			# @TODO: prepare query arguments
			# @TODO: prepare params
			# @TODO: prepare model

			action(opt, opt.model)

class Schema:
	def __init__(self, schema):

		self.schema = {}
		self.keys = []

		# name:type, enum:{enum|enum|enum}, nested:{ name:string, email:email }, array: [ name:String, email: Email ]

	def validate(value, response = None):

		if response == None:
			response = Response()

		# parser
		pass

