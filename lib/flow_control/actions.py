# -*- coding: utf-8 -*-
__authors__="Jesús Zerpa"
actions={}
def add_action(name,fn,priority=9):
	global actions
	if name in actions:
		if priority in actions[name]:
			actions[name][priority].append(fn)
		else:
			actions[name]={priority:[fn]}
	else: 
		actions[name]={priority:[fn]}

def do_action(Supervisor,action,*args,**kwargs):
	global actions
	print("##### haciendo action")
	if action in actions:
		for priority in actions[action]:
				for fn in actions[action][priority]:					
					print(">>>>>> ",action)
					fn(Supervisor,*args,**kwargs)

def action(fn):

	add_action(fn.__name__,fn)	
	return fn