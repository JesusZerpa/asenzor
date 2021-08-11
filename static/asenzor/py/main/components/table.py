__pragma__("alias","s","$")
from .components.vuepy import VuePy 
class ToolBar(VuePy):
	"""docstring for Toolbar"""
	methods=["open_modal"]
	def open_modal(self):
		modal=M.instance(document.querySelector("#media_modal"))
		modal.open()
		

class Table(VuePy):
	"""docstring for Table"""
	def delete(self):
		alert("delete")
	