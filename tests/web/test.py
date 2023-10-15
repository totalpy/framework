import TotalPy

@TotalPy.action({ 'name': 'kokoris', 'input': '*email:Email' })
def action(opt, model):
	pass

print(TotalPy.actions)