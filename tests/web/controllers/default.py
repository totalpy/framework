def install():

	import time

	TotalPy.endpoint('API  /api/  +users_remove --> users/query users/remove')

	@TotalPy.endpoint('GET /')
	def index(ctrl):
		ctrl.plain('index')

	@TotalPy.endpoint('GET /products/{category}/')
	def products(ctrl):
		ctrl.plain('Products: ' + ctrl.params.get('category'))

	@TotalPy.endpoint('GET /admin/...')
	def admin(ctrl):
		ctrl.plain('admin')
