
from django.conf import settings
menus={"ADMIN_MENU":[
		["Formularios",settings.ASENZOR_URL+"forms/","Forms.index","view_list",[]],
		["Paginas",settings.ASENZOR_URL+"pages/","Pages.index","web",[]],
		["Configuracion de paginas",settings.ASENZOR_URL+"page-template/","PageTemplate.index","dashboard",[]],
		["Entradas",settings.ASENZOR_URL+"posts/","Posts.index","post_add",[]],
		["Medios",settings.ASENZOR_URL+"media/","Media.index","perm_media",[]],
		["Plugins",settings.ASENZOR_URL+"plugins/","Plugins.index","settings_suggest",[]],
		["Atencion al cliente",settings.ASENZOR_URL+"support/","Support.index","support",[]],
		["Ajustes",settings.ASENZOR_URL+"options/","Options.index","settings",[]],

		],
	   "ADMIN_NAVBAR":[
	    ["Ir al sitio",settings.BASE_URL,None,None,[]],
	   	["Personalizar",settings.ASENZOR_URL+"customize/",None,None,[]],
	   	["Añadir Pagina",settings.ASENZOR_URL+"posts/new/","Pages.new",None,[]],
	   	["Añadir Fromulario",settings.ASENZOR_URL+"forms/new/","Forms.new",None,[]],
	   	]}#[view,[methods permitidos,{method:index}]]
