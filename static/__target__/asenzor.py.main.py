__pragma__("alias","s","$")
from .asenzor.py.table import Table,ToolBar
from .asenzor.py.media import Media
from .asenzor.py.edit import Edit
from .asenzor.py.plugins import Plugins
from .asenzor.py.support import Support
from .asenzor.py.vuepy import Vue
element=require("element-ui")

element.locale("en")
Vue.use(element)


if document.querySelector("#table_app"):
	window.table=Table().mount("#table")
	window.toolbar=ToolBar().mount("#toolbar")
if document.querySelector("#media_modal"):
	window.media=Media().mount("#media_modal")
	pass
if document.querySelector("#edit_app"):
	window.edit=Edit().mount("#edit_app")
if document.querySelector("#install_plugins"):
	window.plugins=Plugins().mount("#install_plugins")
if document.querySelector("#support_app"):
	window.plugins=Support().mount("#support")
	window.table=Table().mount("#table")
def sticky():
    altura = s('.navbar').offset().top;
    def switch():
        if ( s(window).scrollTop() > altura ):
            s('.navbar').addClass('navbar-fixed');
        else:
            s('.navbar').removeClass('navbar-fixed');
    s(window).on('scroll',switch)
if location.href==ASENZOR_URL:
	fetch("https://zerpatechnology.com.ve/asenzor/json/last-version").then(
		)

s(document).ready(sticky)