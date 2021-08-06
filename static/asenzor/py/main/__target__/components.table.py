__pragma__("alias","s","$")
from .components.vuepy import VuePy 
class ToolBar(VuePy):
	"""docstring for Toolbar"""
	methods=["open_modal"]
	def open_modal(self):
		s("#media_modal").modal("show")

class Table(VuePy):
	"""docstring for Table"""
	def delete(self):
		alert("delete")
	