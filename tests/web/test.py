import TotalPy
import pkg_resources

#package = 'totalpy'
#installed = { pkg.key for pkg in pkg_resources.working_set }
#if package not in installed:
#	print('NOT INSTALLED')

@TotalPy.action('kokotaris', { 'input': '*email:Email' })
def action(opt, model):
	pass

#print(TotalPy.actions)