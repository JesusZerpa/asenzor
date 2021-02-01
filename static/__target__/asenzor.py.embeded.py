__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy
class Embeded(VuePy):
	template="#embeded-template"
	methods=["change"]
	def data(self):
		value=""
		return {"content":value,"name":self.vue["$attrs"]["name"]}
	async def mounted(self):
		root=await edit
		console.log("ffffffff",root)
		self.vue.content=await root.get_content(self.vue["$attrs"]["name"])
	async def change(self):
		await self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue["content"]})

