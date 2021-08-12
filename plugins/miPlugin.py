"""
Este es un plugin de prueba para probar la gestion de plugin de asenzor
"""
__title__="Mi Plugin"
__authors__="Jesus Zerpa"
__version__="0.0.1"
import django
from asenzor.lib.plugins import Plugin
from django.http import JsonResponse

class Plugin(Plugin):
	"""docstring for Plugin"""
	#lista de url de plugins que deben estar instalados para que este pueda funcionar
	# "https://zerpatechnology.com.ve/products/asenzor/plugins/<id>"
	# o ("https://zerpatechnology.com.ve/products/asenzor/plugins/<id>","necesary")
	# si es obligatorio estar instalado
	depenencies=[]
	def __init__(self):
		super(Plugin, self).__init__()
		self.load_hooks()
		print("AAAAAAAAAAAAAAAAAAAAAAA")

	def load_hooks(self):
		self.add_singal("señal_prueba",django.dispatch.Signal(providing_args=["book", "author"]))
		self.add_action("señal_prueba",lambda sender,**kwargs:print("Señal enviada"))
		self.add_filter("prueba",lambda content:content+" modificado desde un filtro")
		self.add_shortcode("shortcode-prueba",lambda *args, **kwargs: "")
	def load_api(self,urlpattern):
		urlpattern.append(
			path("miplugin/",lambda request:JsonResponse({""}) )
			)

