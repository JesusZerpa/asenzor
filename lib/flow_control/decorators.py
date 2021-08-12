def add_action(priority=9):
	def wrapper2(fn):
		from main.flow_control.actions import add_action	
		add_action(fn.__name__,fn,priority=priority)
	return wrapper2
