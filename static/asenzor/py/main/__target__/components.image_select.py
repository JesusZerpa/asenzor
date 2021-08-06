__pragma__("alias","s","$")
from .components.vuepy import VuePy
class ImageSelect(VuePy):
	template="#image-select"
	image=None
	name=None
	methods=["open_modal","remove_img"]
	def data(self):
		return {"image":{"src":""},"name":self.vue["$attrs"]["name"]}
	async def preview(self,result):

		self.vue.image=result[0]
		await self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue.image.src})
	async def remove_img(self):
		self.vue.image=None
		await self.vue["$root"].update_content({self.vue["$attrs"]["name"]:None})
	async def mounted(self):
		vue=self.vue
		value=await vue["$root"].get_content(vue["$attrs"]["name"])
		if value:
			if value:
				image={"src":value}
		else:
			image=vue.image
		vue["image"]=image
		



	async def open_modal(self):
		window.media.single=True
		lib=await media
		console.log(lib)
		lib.vue["$on"]("accept",await self.preview)
		s("#media_modal").modal("show")
		