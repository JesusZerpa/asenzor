
from django.conf import settings
menus={"ADMIN_MENU":[
		["Formularios",settings.ASENZOR_URL+"forms/","Forms.index",None,[]],
		["Paginas",settings.ASENZOR_URL+"pages/","Pages.index",None,[]],
		["Configuracion de paginas",settings.ASENZOR_URL+"page-template/","PageTemplate.index",None,[]],
		["Entradas",settings.ASENZOR_URL+"posts/","Posts.index",None,[]],
		["Medios",settings.ASENZOR_URL+"media/","Media.index",None,[]],
		["Plugins",settings.ASENZOR_URL+"plugins/","Plugins.index",None,[]],
		["Atencion al cliente",settings.ASENZOR_URL+"support/","Support.index",None,[]],
		["Ajustes",settings.ASENZOR_URL+"options/","Options.index",None,[]],

		],
	   "ADMIN_NAVBAR":[
	    ["Ir al sitio",settings.BASE_URL,None,None,[]],
	   	["Personalizar",settings.ASENZOR_URL+"customize/",None,None,[]],
	   	["Añadir Pagina",settings.ASENZOR_URL+"posts/new/","Pages.new",None,[]],
	   	["Añadir Fromulario",settings.ASENZOR_URL+"forms/new/","Forms.new",None,[]],
	   	]}#[view,[methods permitidos,{method:index}]]
