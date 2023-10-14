# JSON schema validators
# The MIT License
# Copyright 2023 (c) Peter Širka <petersirka@gmail.com>

import TotalPy
import re
import datetime

def check_string(meta, error, value, errplus, path):

	if value == None:
		value = ''
	elif type(value) is not str:
		value = str(value)

	length = len(value)

	if length > 0:
		match meta.get('subtype'):
			case 'name':
				value = utils.convert(value, 'name')

	if meta.get('REQUIRED') != False and length == 0:
		error.push(errplus + meta['ID'], None, path)
		return

	if meta.get('maxLength') != None and length > meta['maxLength']:
		error.push(errplus + meta['ID'], None, path)
		return

	if meta.get('minLength') != None and length < meta['minLength']:
		error.push(errplus + meta['ID'], None, path)
		return

	if length > 0:
		match meta.get('subtype'):
			case 'email':
				value = TotalPy.utils.convert(value, 'email')
				if TotalPy.utils.validate(value, 'email') == False:
					error.push(errplus + meta['ID'], None, path)
					return

			case 'phone':
				value = TotalPy.utils.convert(value, 'phone')
				if TotalPy.utils.validate(value, 'phone') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'url':
				if TotalPy.utils.validate(value, 'url') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'zip':
				if TotalPy.utils.validate(value, 'zip') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'guid':
				if TotalPy.utils.validate(value, 'guid') == False:
					error.push(errplus + meta['ID'], None, path)
					return
				elif value == '':
					value = None
			case 'uid':
				if TotalPy.utils.validate(value, 'uid') == False:
					error.push(errplus + meta['ID'], None, path)
					return
				elif value == '':
					value = None
			case 'json':
				if TotalPy.utils.validate(value, 'json') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'base64':
				if TotalPy.utils.validate(value, 'base64') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'color':
				if TotalPy.utils.validate(value, 'color') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'icon':
				if TotalPy.utils.validate(value, 'icon') == False:
					error.push(errplus + meta['ID'], None, path)
					return
			case 'lower' | 'lowercase':
				value = value.lower()
			case 'upper' | 'uppercase':
				value = value.upper()
			case 'capitalize':
				value = value.capitalize()

	if (value != '' or meta.get('REQUIRED') == True) and meta.get('enum') != None:
		if meta['enum'].find(value) == -1:
			error.push(errplus + meta['ID'], None, path)
			return

	return value

def check_number(meta, error, value, errplus, path):

	subtype = meta.get('subtype')

	if value != None:
		t = type(value)
		if subtype == None or subtype == 'float' or subtype == 'decimal' or subtype == 'number':
			value = TotalPy.utils.convert(value, 'float')
		else:
			value = TotalPy.utils.convert(value, 'int')

	if meta.get('REQUIRED') != False:
		if value == None:
			error.push(errplus + meta['ID'], None, path)
			return

	if value == None:
		return

	if meta.get('multipleOf') != None and value % meta['multipleOf'] != 0:
		error.push(errplus + meta['ID'], None, path)
		return

	if meta.get('maximum') != None and value > meta['maximum']:
		error.push(errplus + meta['ID'], None, path)
		return

	if meta.get('exclusiveMaximum') != None and value >= meta['exclusiveMaximum']:
		error.push(errplus + meta['ID'], None, path)
		return

	if meta.get('minimum') != None and value < meta['minimum']:
		error.push(errplus + meta['ID'], None, path)
		return

	match meta.get('subtype'):
		case 'smallint':
			if value < -32767 or value > 32767:
				error.push(errplus + meta['ID'], None, path)
				return
		case 'tinyint':
			if value < 0 or value > 255:
				error.push(errplus + meta['ID'], None, path)
				return

	if meta.get('exclusiveMinimum') != None and value <= meta['exclusiveMinimum']:
		error.push(errplus + meta['ID'], None, path)
		return

	return value


def check_boolean(meta, error, value, errplus, path):

	t = type(value)

	if t is str:
		value = TotalPy.utils.convert(value, 'bool')
	elif t is int or t == float:
		value = value != 0

	if meta.get('REQUIRED') != False and value == None:
		error.push(errplus + meta['ID'], None, path)
		return

	if value != None:
		return value

def check_date(meta, error, value, errplus, path):

	if isinstance(value, datetime.date) == False:
		t = type(value)
		if t is str or t is int:
			value = TotalPy.utils.convert(value, 'datetime')
		else:
			value = None

	if meta.get('REQUIRED') != False and value == None:
		error.push(errplus + meta['ID'], None, path)
		return

	if value != None:
		return value;

def check_array(meta, error, value, stop, definitions, path):

	if value is not list:
		if meta.get('REQUIRED') != False:
			error.push(meta['ID'], None, path)
		return

	if len(value) == 0:
		if meta.get('REQUIRED') != False:
			error.push(meta['ID'], None, path);
			return
		return value

	currentpath = path;

	if meta.get('items') != None:

		response = [];

		for index in range(0, len(value)):

			val = value[index];

			match meta['items'].get('type'):
				case 'number' | 'integer':
					tmp = check_number(meta['items'], error, val, None, currentpath)
					if tmp != None and (meta.get('uniqueItems') == None or response.find(tmp) == -1):
						response.append(tmp)
				case 'boolean' | 'bool':
					tmp = check_boolean(meta['items'], error, val, None, currentpath)
					if tmp != None and (meta.get('uniqueItems') == None or response.find(tmp) == -1):
						response.push(tmp)
				case 'date':
					tmp = check_date(meta['items'], error, val, None, currentpath)
					if tmp != None and (meta.get('uniqueItems') == None or response.find(tmp) == -1):
						response.push(tmp)
				case 'object':
					tmpresponse = TotalPy.builders.Response()
					tmp = check_object(meta['items'], tmpresponse, val, stop, definitions, currentpath)
					if tmpresponse.errors.length > 0:
						for err in tmpresponse.errors:
							error.push(meta['ID'] + '.' + err.name, err.error, currentpath, index)
					if tmp != None and (meta.get('uniqueItems') == None or response.find(tmp) == -1):
						response.push(tmp)
				case 'array':
					tmp = check_array(meta['items'], error, value, stop, definitions, currentpath);
					if tmp != None and (meta.get('uniqueItems') == None or response.find(tmp) == -1):
						response.push(tmp);
				case _:
					tmp = check_string(meta['items'], error, val, null, currentpath);
					if tmp != None and (meta.get('uniqueItems') == None or response.find(tmp) == -1):
						if (tmp == None or tmp == '') and meta['items'].get('subtype') == 'uid':
							tmp = None
						response.push(tmp)
	else:
		# response = meta.uniqueItems ? [...new Set(value)] : value;
		pass

	if length(response) == 0 and meta['REQUIRED'] != None:
		error.push(meta['ID'], None, currentpath)
		return

	if meta.get('minItems') and len(response) < meta['minItems']:
		error.push(meta['ID'], None, currentpath)
		return

	if meta.get('maxItems') and len(response) < meta['maxItems']:
		error.push(meta['ID'], None, currentpath)
		return

	return response

def check_object(meta, error, value, response, stop, definitions, path):

	if value == None or type(value) is not dict:
		if meta.get('REQUIRED') != False:
			error.push(errplus + meta['ID'], None, path)
		return

	if stop == True and len(error.errors) > 0:
		return

	if meta.get('properties') == None:
		return value

	if response == None:
		response = {}

	count = 0

	for key in meta['properties']:

		prop = meta['properties'][key]

		if prop.get('ID') == None:
			prop['ID'] = key
			prop['REQUIRED'] = False
			if meta.get('required') != None and key in meta['required']:
				prop['REQUIRED'] = True

		if stop == True and len(error.errors) > 0:
			return

		if meta.get('maxProperties') != None and count > meta['maxProperties']:
			error.push(meta['ID'], None, path)
			return

		currentpath = ''

		if path != None and len(path) > 0:
			currentpath = path + '.' + key
		else:
			currentpath = key

		val = value.get(key)

		match prop['type']:
			case 'number' | 'integer':
				tmp = check_number(prop, error, val, '', currentpath)
				if tmp != None:
					response[key] = tmp
					++count
			case 'boolean' | 'bool':
				tmp = check_boolean(prop, error, val, '', currentpath)
				if tmp != None:
					response[key] = tmp
					++count
				break;
			case 'date':
				tmp = check_date(prop, error, val, '', currentpath)
				response[key] = tmp
				++count
			case 'string':
				tmp = check_string(prop, error, val, '', currentpath)
				if tmp != None:
					if tmp != '' and prop.get('subtype') == 'uid':
						tmp = None
					response[key] = tmp
					++count
			case 'object':
				if prop.get('properties') != None:
					tmp = check_object(prop, error, val, None, None, definitions, currentpath)
					if tmp != None:
						response[key] = tmp;
						++count
			case 'array':
				tmp = check_array(prop, error, val, None, definitions, currentpath);
				if tmp != None:
					response[key] = tmp
					++count
			case _:
				tmp = check_string(prop, error, val, '', currentpath);
				if tmp != None:
					if tmp != '' and prop.get('subtype') == 'uid':
						value = None
					response[key] = tmp
					++count

	if meta.get('minProperties') and count < meta['minProperties']:
		error.push(meta['ID'], None, path)
		return

	return response

def read(ref, definitions):
	if ref[0] == '#':
		tmp = ref[2:].split('/')
		definition = definitions.get(tmp[0])
		if definition != None:
			schema = tmp[1]
			obj = definition.get('schema')
			if obj != None:
				if obj.get('ID') == None:
					obj['ID'] = schema
				return obj

def transform(meta, response, value, stop = True, path = ''):

	if response == None:
		response = TotalPy.builders.Response()

	output = None

	match meta['type']:
		case 'string':
			output = check_string(meta, response, value, '', path);
		case 'number' | 'integer' | 'float' | 'decimal':
			output = check_number(meta, response, value, '', path);
		case 'boolean' | 'bool':
			output = check_boolean(meta, response, value, '', path);
		case 'date':
			output = check_date(meta, response, value, '', path);
		case 'object':
			output = check_object(meta, response, value, None, stop, meta, path);
		case 'array':
			output = check_array(meta, response, value, stop, meta, path);
		case _:
			error.push('.type', undefined, path);

	if stop == True and len(response.errors) > 0:
		response.response = {}
		return response

	if output == None:
		output = {}

	response.response = output;
	return response