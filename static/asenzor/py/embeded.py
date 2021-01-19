__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy
class Embeded(VuePy):
	template="#embeded-template"
	methods=["change"]
	def data(self):
		value=edit.get_content(self.vue["$attrs"]["name"])
		return {"content":value,"name":self.vue["$attrs"]["name"]}
	def change(self):
		self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue["content"]})

