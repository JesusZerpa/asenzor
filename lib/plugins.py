class Plugin:
	def __init__(self,
			urlpattern,
			apipatterns,
			menus):
		self.load_hooks()
		self.load_apis(apipatterns)
		self.load_views(urlpattern)
		self.add_menus(menus)

	def add_signal(self,name,signal):
		pass
	def add_shortcode(self,name,fn):
		pass
	def add_filter(self,name,fn):
		pass
	def add_action(self,name,fn):
		pass
	def load_hooks():
		pass 
	def load_views(self,urlpattern):
		pass 
	def load_apis(self,urlpattern):
		pass
	def add_menus(self,menus):
		pass
