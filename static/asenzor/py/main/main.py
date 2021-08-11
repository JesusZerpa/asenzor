__pragma__("alias","s","$")
from .components.table import Table,ToolBar
from .components.media import Media
from .components.edit import Edit
from .components.plugins import Plugins
from .components.support import Support
from .components.vuepy import Vue

element=require("element-ui")
lang=require('element-ui/lib/locale/lang/en')
locale=require('element-ui/lib/locale')
element.locale("en")
Vue.use(element)

async def main():
	if document.querySelector("#table_app"):
		window.table=await Table().mount("#table")
		window.toolbar=await ToolBar().mount("#toolbar")
	if document.querySelector("#media_modal"):
		window.media=await Media().mount("#media_modal")
		pass
	if document.querySelector("#edit_app"):
		window.edit=await Edit().mount("#edit_app")
	if document.querySelector("#install_plugins"):
		window.plugins=await Plugins().mount("#install_plugins")
	if document.querySelector("#support_app"):
		window.plugins=await Support().mount("#support")
		window.table=await Table().mount("#table")
	"""
	def sticky():
	    altura = s('.navbar').offset().top;
	    def switch():
	        if ( s(window).scrollTop() > altura ):
	            s('.navbar').addClass('navbar-fixed');
	        else:
	            s('.navbar').removeClass('navbar-fixed');
	    s(window).on('scroll',switch)
	"""
	if location.href==ASENZOR_URL:
		fetch("https://zerpatechnology.com.ve/asenzor/json/last-version").then(
			)
main()
#s(document).ready(sticky)