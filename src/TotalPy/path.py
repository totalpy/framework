# Paths

import TotalPy
import os
import sys

def root(filename = ''):
	return os.path.join(TotalPy.directory, filename)

def __internal(dir, filename):
	# TODO: check directory
	return os.path.join(TotalPy.directory, dir, filename)

def bundles(filename = ''):
	return __internal('bundles', filename)

def databases(filename = ''):
	return __internal('databases', filename)

def modules(filename = ''):
	return __internal('modules', filename)

def public(filename = ''):
	return __internal('public', filename)

def definitions(filename = ''):
	return __internal('definitions', filename)

def plugins(filename = ''):
	return __internal('plugins', filename)

def flowstreams(filename = ''):
	return __internal('flowstreams', filename)

def schemas(filename = ''):
	return __internal('schemas', filename)

def resources(filename = ''):
	return __internal('resources', filename)

def actions(filename = ''):
	return __internal('actions', filename)

def controllers(filename = ''):
	return __internal('controllers', filename)

def temp(filename = ''):
	return __internal('tmp', filename)

def tmp(filename = ''):
	return __internal('tmp', filename)

def join(a, b):
	return os.path.join(a, b)