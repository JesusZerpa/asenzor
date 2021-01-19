__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy
class ImageSelect(VuePy):
	template="#image-select"
	image=None
	name=None
	methods=["open_modal","remove_img"]
	def data(self):

		value=self.vue["$root"].get_content(self.vue["$attrs"]["name"])
		if value:
			if value:
				image={"src":value}
		else:
			image=self.image
		return {"image":image,"name":self.vue["$attrs"]["name"]}
	def preview(self,result):

		self.vue.image=result[0]
		self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue.image.src})
	def remove_img(self):
		self.vue.image=None
		self.vue["$root"].update_content({self.vue["$attrs"]["name"]:None})
	def mounted(self):
		pass

	def open_modal(self):
		window.media.single=True
		window.media.vue["$on"]("accept",self.preview)
		s("#media_modal").modal("show")
		