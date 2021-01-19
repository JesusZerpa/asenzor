__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy

class Support(VuePy):
	"""docstring for Support"""
	methods=["change","update_token"]
	def data(self,):
		return {"parner":DATA["parner"]}
	def change(self):
		self.vue["$refs"]["parner_token"].disabled=False
	async def update_token(self):
		form=__new__(FormData())
		form.append("parner_token",self.vue["$refs"]["parner_token"].value)
		req=await fetch(ASENZOR_URL+"json/support/change-parner",{
			"body":form,
			"method":"PATCH",
			})
		data=req.json()
		self.vue["parner"]=data["item"]
		self.vue["$refs"]["parner_token"].disabled=True