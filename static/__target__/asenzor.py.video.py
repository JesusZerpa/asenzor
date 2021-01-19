__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy 
class Video(VuePy):
	"""docstring for Toolbar"""
	methods=["update_video"]
	template="""<div>
	<iframe :src="video" style="max-width:100%"/>
	<input :ref="'video'" @change="update_video"/>
	</div>
	"""
	def data(self):
		name=self.vue["$attrs"]["name"]
		#video=self.vue["$root"].get_content(name)
		video=None
		return {"video":video,"name":name}

	def update_video(self):
		self.vue.video=self.vue["$refs"]["video"].value
		self.vue["$root"].update_content({self.vue["name"]:self.vue.video})
