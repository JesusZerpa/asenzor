
class Filters(object):
	"""
	Los filtros son el tipo de hook que son usados para 
	mostrar contenido, este no tiene nada que ver con los action
	que son eventos que se manejan cuando se hace un POST o un GET

	"""
	def __init__(self):
		super(Filters, self).__init__()
		self.hooks={}
	def has_filter(self,filtro):
		return filtro in  self.filters
	def add_filter(self,hook_name,function=None,priority=10,accepted_args=1):
		if type(hook_name)==str and function!=None:
			
			if hook_name not in self.hooks:
				self.hooks[hook_name]={priority:[function]}
			else:
				if priority not in self.hooks[hook_name]:
					self.hooks[hook_name][priority]=[]
				self.hooks[hook_name][priority].append(function)
			
			
		else:
			"""
			if action.func_name not in self.hooks:
				self.hooks[action.func_name]=[action]

			self.hooks[action.func_name].insert(priority,action)
			"""
		
		def funcion(*args,**kwargs):
			return self.apply_filters(action.func_name,*args,**kwargs)

		return funcion

	def apply_filters(self,hook_name,result=None,*args,**kwargs):
		if hook_name in self.hooks:
			l=list(self.hooks[hook_name])
			
			for priority in l:
				for elem in self.hooks[hook_name][priority]:
					result=elem(result,*args,**kwargs)
		return result

	def apply_filters_ref_array(self):
		pass
	def current_filter(self):
		pass
	def remove_filter(self):
		pass
	def remove_all_filter(self):
		pass

	def doing_filter(self):
		pass
filters=Filters()

	