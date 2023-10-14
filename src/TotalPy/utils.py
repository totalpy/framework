# Utils

from urllib.parse import unquote
import base64
import json
import re
import random
import os
import math
import datetime
import numpy as np

RANDOM_STRING = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
RANDOM_NUMBER = list('0123456789')
RANDOM_TEXT = RANDOM_NUMBER + RANDOM_STRING
RANDOM_BASE = RANDOM_NUMBER + list('abcdefghijklmnopqrstuvwxyz')

REG_NUMBER = re.compile(r'[\d,.]+');
REG_COLOR = re.compile(r'^#([A-F0-9]{3}|[A-F0-9]{6}|[A-F0-9]{8})$');
REG_ICON = re.compile(r'^(ti|far|fab|fad|fal|fas|fa)?\s(fa|ti)-[a-z0-9-]+$');
REG_INT = re.compile(r'[0-9\s]+')
REG_FLOAT = re.compile(r'[0-9,.\s]+')
REG_PHONE_CLEAN = re.compile(r'[^0-9-\+]')
REG_PHONE = re.compile(r'^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,8}$')
REG_EMAIL = re.compile(r'^[a-zA-Z0-9-_.+]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$', re.IGNORECASE)
REG_ZIP = re.compile(r'^[0-9a-z\-\s]{3,20}$', re.IGNORECASE)
REG_UID = re.compile(r'^\d{14,}[a-z]{3}[01]{1}|^\d{9,14}[a-z]{2}[01]{1}a|^\d{4,18}[a-z]{2}\d{1}[01]{1}b|^[0-9a-f]{4,18}[a-z]{2}\d{1}[01]{1}c|^[0-9a-z]{4,18}[a-z]{2}\d{1}[01]{1}d|^[0-9a-zA-Z]{5,10}\d{1}[01]{1}f|^[0-9a-zA-Z]{10}[A-J]{1}r$')
REG_URL = re.compile(r'http(s)?:\/\/[^,{}\\]*$')
REG_COLOR = re.compile(r'^#([A-F0-9]{3}|[A-F0-9]{6}|[A-F0-9]{8})$', re.IGNORECASE)
REG_ICON = re.compile(r'^(ti|tic|far|fab|fad|fal|fas|fa)?\s(fa|ti)-[a-z0-9-]+$');

def random_text(max):
	builder = '';
	for i in range(max):
		builder += random.choice(RANDOM_TEXT)
	return builder;

def random_string(max):
	builder = '';
	for i in range(max):
		builder += random.choice(RANDOM_STRING)
	return builder;

def random_number(max):
	builder = '';
	for i in range(max):
		c = random.choice(RANDOM_NUMBER)
		if (c == '0'):
			c = '1'
		builder += c
	return builder

def parseuid(value):
	pass

def parsedate(value):
	pass

def parsejson(value):
	pass

def int2str(value, base = 62):

	residual = math.floor(value);
	str = None

	match base:
		case 16:
			str = RANDOM_BASE[0:16]
		case 32:
			str = RANDOM_BASE[0:32]
		case 36:
			str = RANDOM_BASE[0:36]
		case 62:
			str = RANDOM_TEXT

	result = '';

	while True:
		rixit = residual % base
		result = str[rixit] + result
		residual = math.floor(residual / base)
		if (residual <= 0):
			break

	return result

def str2int(value, base = 62):

	result = 0

	match base:
		case 16:
			str = RANDOM_BASE[0:16]
		case 32:
			str = RANDOM_BASE[0:32]
		case 36:
			str = RANDOM_BASE[0:36]
		case 62:
			str = RANDOM_TEXT

	for c in list(value):
		result = (result * base) + str.index(c)

	return result

def parsedate(value):
	# @TODO: missing implementation
	pass

def parseuri(path):

	index = path.find('?', 1)
	response = {}

	if index != -1:
		args = path[index + 1:].split('&')
		response['pathname'] = path[0:index]
		response['query'] = {}
		for m in args:
			arr = m.split('=')
			response['query'][arr[0]] = unquote(arr[1])
	else:
		response['pathname'] = path

	response['file'] = response['pathname'].find('.', len(response['pathname']) - 8) != -1

	if response['file'] == False:
		if response['pathname'][len(response['pathname']) - 1] != '/':
			response['pathname'] = response['pathname'] + '/'

	response['url'] = response['pathname']
	return response

def parseua(value):
	# @TODO: missing implementation
	pass

def parseconfig(value):

	response = {}
	lines = value.split('\n')
	for line in lines:

		# Comment
		if line.strip()[0:2] == '//':
			continue

		index = line.find(':', 2)
		key = line[0:index].strip()
		value = line[index + 1:].strip()
		type = 'string'

		index = key.find('(')

		if index != -1:
			type = key[index + 1:].lower().replace(')', '').strip()
			key = key[0:index].strip()

		if value[0:7] == 'base64 ':
			value = base64.b64decode(value[7:].strip()).decode('utf8')
		elif value[0:4] == 'hex ':
			value = bytes.fromhex(value[4:]).decode('utf8')

		match type:
			case 'generate':
				# generate persistent values
				pass
			case 'random':
				value = int(value)
				value = random_string(value)
				pass
			case 'date':
				# @TODO: missing date parser
				pass
			case 'object':
				value = json.loads(value)
				pass
			case 'env':
				value = os.getenv(value)
				pass
			case 'number':
				if re.search('\.|\,', tmp) != None:
					value = float(value)
				else:
					value = int(value)
			case 'boolean':
				tmp = value.lower()
				if tmp == 'true' or tmp == 'on' or tmp == '1':
					value = True
				else:
					value = False
			case _:
				tmp = value.lower()
				if tmp == 'false' or tmp == 'true':
					value = tmp == 'true'
				elif re.search('^[0-9,.]+$', tmp):
					tmp = tmp.replace(',', '.')
					if tmp.find('.') != -1:
						value = float(tmp)
					else:
						value = int(tmp)

		response[key] = value

	return response

def parsejsonschema(value):

	obj = {}
	obj['type'] = 'object'
	obj['properties'] = {}

	nestedtypes = []
	required = []

	# Objects
	matches = re.findall(r'\{.*?\}', value)
	for text in matches:
		index = len(nestedtypes)
		nestedtypes.append(text[1:len(text) - 1])
		value = value.replace(text, '{#' + str(index) + '}')

	# Arrays
	matches = re.findall(r'\[.*?\]', value)
	for text in matches:
		index = len(nestedtypes)
		nestedtypes.append(text[1:len(text) - 1])
		value = value.replace(text, '[#' + str(index) + ']')

	properties = re.split(r',|\n', value)

	for prop in properties:

		arr = prop.split(':')

		name = arr[0].strip()
		type = 'string'
		size = 0
		nestedschema = ''

		if len(arr) > 1:
			type = arr[1].strip().lower()

		if name[0] == '!' or name[0] == '*':
			name = name[1:]
			required.append(name)

		isarr = type[0] == '['

		if isarr:
			type = type[1:len(type) - 1]

		isenum = type[0] == '{'
		if isenum:
			tmp = type[2:len(type) - 1]
			tmp = nestedtypes[int(tmp)]
			if tmp.find(':') != -1:
				type = 'object'
				nestedschema = parsejsonschema(tmp)
			else:
				type = 'enum'
				enums = re.split(r';|\|/', tmp)
				for index in range(0, len(enums)):
					enums[index] = enums[index].strip()

		index = type.find('(')

		if index != -1:
			size = int(type[index + 1:len(type) - 1].strip())
			type = type[0:index].strip()

		if type[0] == '#':
			type = nestedtypes[int(type[1:])]
			if type[0] == '{':
				isenum = True
				type = type[1:len(type) - 1]
			elif re.search(r':|,|\n', type) != None:
				isenum = True

			# Is nested object? {...}
			if isenum:
				nestedschema = parsejsonschema(type)
				type = 'object'
			else:
				type = type.lower()
		elif type[0] == '@':
			# type = 'object'
			raise Exception('Not implemented schemas')

		tmp = None

		match type:
			case 'string' | 'uid' | 'guid' | 'email' | 'phone' | 'name' | 'url' | 'zip' | 'lower' | 'upper' | 'lowercase' | 'uppercase' | 'capitalize' | 'capitalize2' | 'color' | 'icon' | 'base64':
				tmp = {}
				if isarr:
					tmp['type'] = 'array'
					tmp['items'] = { 'type': 'string', 'subtype': None }

					if type != 'string':
						tmp['items']['subtype'] = type

					if size > 0:
						tmp['items']['maxLength'] = size
				else:
					tmp['type'] = 'string'
					if type != tmp['type']:
						tmp['subtype'] = type
					if size > 0:
						tmp['maxLength'] = size

			case 'number' | 'number2' | 'float' | 'decimal' | 'int' | 'integer' | 'smallint' | 'tinyint':

				if type == 'integer':
					type = 'int'

				tmp = {}

				if isarr:
					tmp['type'] = 'array'
					tmp['items'] = { 'type': 'number', 'subtype': None }
					if type != 'number':
						tmp['items']['subtype'] = type
				else:
					tmp['type'] = 'number'
					if type != 'number':
						tmp['subtype'] = type

			case 'bool' | 'boolean':
				tmp = {}
				if isarr:
					tmp['type'] = 'array'
					tmp['items'] = { 'type': 'boolean' }
				else:
					tmp['type'] = 'boolean'

			case 'date':
				tmp = {}
				if isarr:
					tmp['type'] = 'array'
					tmp['items'] = { 'type': 'date' }
				else:
					tmp['type'] = 'date'

			case 'object':
				tmp = {}
				if isarr:
					tmp['type'] = 'array';
					if nestedschema == '':
						tmp['items'] = { 'type': 'object' }
					else:
						tmp['items'] = { 'type': nestedschema }
				elif nestedschema:
					tmp = nestedschema
				else:
					tmp['type'] = 'object'

			case 'enum':
				tmp = { 'enum': tmp, 'type': 'string' };

			case _:
				tmp = {}
				if isarr:
					tmp['type'] = 'array';
					tmp['items'] = { 'type': 'string' };
				else:
					tmp['type'] = 'string';

		if tmp != None:
			obj['properties'][name] = tmp;

	if len(required) > 0:
		obj['required'] = required;

	return obj


def minifycss(value):
	pass

def minifyjs(value):
	pass

def minifyhtml(value):
	pass

def radix(number, base):

	base = 16
	radix = RADIX16

	if number < base:
		return radix[number]
	else:
		return radix(number // base, base) + radix[number % base]

def hash(text):

	hash = np.int32(0.0)
	length = len(text)

	if length == 0:
		return ''

	for i in range(0, length):
		char = ord(text[i])
		hash = np.int32(((np.int32(hash * 2**5)) - hash) + char)

	return int(hash)

def guid(max = None):
	# @TODO: missing implementation
	return ''

def validate(value, target):
	match target:
		case 'color':
			return REG_COLOR.search(value) != None
		case 'icon':
			return REG_ICON.search(value) != None
		case 'email':
			return REG_EMAIL.search(value) != None
		case 'phone':
			return REG_PHONE.search(value) != None
		case 'zip':
			return REG_ZIP.search(value) != None
		case 'uid':
			# @TODO: missing advanced implementation
			return REG_UID.search(value) != None
		case 'url':
			return REG_URL.search(value) != None
		case 'json':
			# @TODO: missing implementation
			return True
		case 'guid':
			# @TODO: missing implementation
			return True
		case 'base64':
			# @TODO: missing implementation
			return True

	return True

def convert(value, target, default = None):
	# types: name, email, phone, int, float, number, date
	t = None
	match target:
		case 'email':
			if type(value) is str:
				return value.lower().strip()
			return default
		case 'phone':
			if type(value) is str:
				return REG_PHONE_CLEAN.sub(value, '')
			return default
		case 'int' | 'integer':
			t = type(value)
			if t is int:
				return value
			elif t is str:
				try:
					m = REG_INT.search(value)
					if m != None:
						return int(m[0].replace(' ', ''))
					return default
				except:
					return default
		case 'number' | 'float' | 'decimal':
			t = type(value)
			if t is float:
				return value
			elif t is str:
				try:
					m = REG_FLOAT.search(value)
					if m != None:
						return float(m[0].replace(' ', ''))
					return default
				except:
					return default
		case 'date' | 'datetime' | 'ts' | 'time':
			return default

	return value
