from django.shortcuts import render
from .lib.ResourceView import ResourceView,serialize,login_required
from .models import *
from .forms import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.http import HttpResponse,HttpResponseRedirect
from django.apps import apps
# Create your views here.
asenzor=apps.get_app_config('asenzor')


@cache_page(0)
@login_required
def dashboard(request):
	cards=[
	{"title":"Bienvenido a ASENZOR",
	 "message":"Tu panel de administración personalizado"}
	]
	return render(request,"asenzor/layouts/dashboard.html",locals())

class Pages(ResourceView):
	"""docstring for Pages"""
	model=Post
	filter={"type":"page"}
	new_template="asenzor/post.html"
	edit_template="asenzor/post.html"
	custom_data={
	"new":{"post_builder":"post",
		   "post_type":"page",
		   "templates":asenzor.get_templates()},
	"edit":{"post_type":"page",
			"templates":asenzor.get_templates()},
	}
	list_display=["title","name","status","author","modified"]
	@classmethod
	def middleware(cls,view,request,data,id=None):
		if view=="edit":
			from .widgets import templates
			post=cls.model.objects.get(id=id)
			template=PostMeta.get(post,"template")
			data["form"]=None
			data["VUE_TEMPLATES"]=templates

			data["post"]=serialize(post)
			data["meta"]={}
			if template:
				templates=asenzor.get_templates()
				if template in templates:
					page=templates[template]
				else:
					page={}

				if page:
					data["post_builder"]="custom"
				else:
					data["post_builder"]="post"
			else:
				data["post_builder"]="post"

			for elem in PostMeta.objects.filter(post=post):

				if elem.key in data["meta"]:
					if type(data["meta"][elem.key])==list:
						data["meta"][elem.key].append(json.loads(elem.value))
					else:
						data["meta"][elem.key]=[
							data["meta"][elem.key],
							json.loads(elem.value)]
				else:
					data["meta"][elem.key]=json.loads(elem.value)

			if data["post"]["content"]==None or data["post"]["content"]=="":
				#si la pagina tiene un template asignado 
				#lee la configuracion del template
				if template: 
					print("AAAAAAAAAAAAA")
					data["post"]["content"]=asenzor.serialize_template_admin_settings(template,request)
					data["page"]=asenzor.compile_template_admin_settings(template,request,data["post"]["content"])
			
			else:
				try:
					
					data["post"]["content"]=json.loads(data["post"]["content"])
					print("BBBBBBBBBBBBBBB",data["post"]["content"]["header"].keys())
					data["page"]=asenzor.compile_template_admin_settings(template,request,data["post"]["content"])
				except Exception as e:
					if data["post_builder"]=="custom":
						print("CCCCCCCCCCCCCCC")
						data["post"]["content"]=asenzor.serialize_template_admin_settings(template,request)
						data["page"]=asenzor.compile_template_admin_settings(template,request,data["post"]["content"])


					
			"""
			data_content=False
			if data["post_builder"]=="custom":
				
				if data["post"]["content"]==None or data["post"]["content"]=="":#
					#si esta vacio
					data["post"]["content"]=asenzor.serialize_template_admin_settings(template,request) 
					
				
					
					data["post"]["content"]=asenzor.serialize_template_admin_settings(template,request) 
				else:#si no esta vacio pero no tiene datos,solo la estructura
					
					try:
						data["post"]["content"]=json.loads(data["post"]["content"])
						data["page"]=asenzor.compile_template_admin_settings(template,request,data["post"]["content"])
					except:
						#elimina el conteido y crea uno nuevo en base a la estructura
						data["post"]["content"]=asenzor.serialize_template_admin_settings(template,request) 
			
			print(data["post"]["content"])
			"""
			print("hhhhhhhh",data["page"]["header"].keys())
			data["DATA"]["post"]=data["post"]
			data["DATA"]["meta"]=data["meta"]
		if view=="new":
			data["post"]={"type":"page"}



class PageTemplate(ResourceView):
	"""docstring for Pages"""
	model=Post
	filter={"type":"page"}
	form=PageTemplateForm
	edit_action=""
	edit_novalidate=True
	list_display=["title","name","status","author","modified"]



class Forms(ResourceView):
	"""docstring for Pages"""
	model=Post
	filter={"type":"form"}

class Support(ResourceView):
	"""docstring for Pages"""
	model=Post
	filter={"type":"support"}
	index_template="asenzor/widgets/support.html"


class Posts(ResourceView):
	"""docstring for Pages"""
	model=Post
	filter={"type":"post"}
	custom_data={
	"new":{"post_builder":"post",
		   "post_type":"post",
		   "templates":asenzor.get_templates()},
	"edit":{"post_builder":"custom",
			"post_type":"post",
			"templates":asenzor.get_templates()},
	}


	

class Media(ResourceView):
	"""docstring for Pages"""
	model=Post
	filter={"type":"attachment"}
	def index(self,request):
		toolbar={
		"btn_media_enabled":True
		}
		return super().index(request,data=locals())

class Options(ResourceView):
	"""docstring for Pages"""
	model=Option
	@classmethod
	def middleware(cls,view,request,data,id=None):
		from django.apps import apps
		asenzor=apps.get_app_config("asenzor")
		if request.method=="POST" and (view=="new" or view=="edit"):
			
			if data["instance"].encrypted:
				data["instance"].value=asenzor.encode(data["instance"].value,asenzor.get_secret_key())
				data["instance"].save()
		elif request.method=="GET":
			if view=="edit":

				if data["instance"].encrypted:
				
					value=data["form"].initial["value"]

					data["form"].initial["value"]=asenzor.decode(value,asenzor.get_secret_key())
			elif view=="show":
				if data["instance"].encrypted:
					data["item"]["value"]=asenzor.decode(data["item"]["value"],asenzor.get_secret_key())
			

@login_required
def preview(request,id):
	page=Post.objects.get(id=id)
	postmeta=PostMeta
	template=postmeta.get(id,"template","index.html")
	return render(request,template,locals())

def install(request):
	print("oooo")
	form=InstallForm()

	if request.method=="GET":
		if len(Site.objects.all()):
			return HttpResponseRedirect(settings.ASENZOR_URL)
		else:
			return render(request,"asenzor/install.html",locals())
	elif request.method=="POST":
		if request.user.is_authenticated:

			main_site=request.POST.get("main_site")
			site_description=request.POST.get("site_description")
			
			site=Site.objects.create(name=main_site,
								domain=request.get_host(),
								description=site_description)
			Site.update_master(site)
			site.save()
			post=Post.objects.create(
				title="Pagina de inicio",
				name="home",
				type="page",
				author=request.user,
				guid="")
			post.save()
			post2=Post.objects.create(
				title="Pagina de blog",
				name="blog",
				type="page",
				author=request.user,
				guid="blog")
			post2.save()
			Option.update("frontpage",post.id)
			Option.update("postpage",post2.id)
			Option.update("smtp_server","smtp.gmail.com",description="Servidor de correo electronico")
			Option.update("smtp_port","587")
			Option.update("sender_email","asenzor@example.com",description="Correo desde donde se manada el mensaje")
			Option.update("owner_email","asenzor@example.com",description="Correo al que se le manda el mensaje")
			Option.update("smtp_password","",encrypted=True,description="Password del servidor de correo ")
			Option.update("recaptcha_secret","",encrypted=True,description="Clave secreta de para formularios con recaptcha")
			
			
			

			return HttpResponseRedirect(settings.ASENZOR_URL)
		else:
			from django.template import Template, Context
			user=User.objects.first()
			t = Template("""Necesitas estar logeado,{{message}}  o accede a  
			 <a href="{{url}}">Login</a>""")
			c = Context({
				"url":settings.BASE_URL+"admin/",
				"message":"prueba ejecutar: python manage.py createsuperuser y luego " if not user else ""	})
			return HttpResponse(t.render(c))


class CustomizeUser(ResourceView):
	"""docstring for Pages"""
	model=User
	forbidden=["index","delete","new"]
	modelmeta=UserMeta
	metafields=[]

class Plugins(ResourceView):
	paginator=None
	new_template="asenzor/plugins.html"
	custom_data={"index":{
	"items":[]
	}}
	
	def paginator(cls,items,pagination):
		class Pagination(list):
			_page=1
			def __init__(self,*args,**kwargs):
				super().__init__(*args,**kwargs)
				self.num_pages=int(len(items)/pagination)
				self.object_list=items
			def page(self,n):
				return type("page",(),{"object_list":self.object_list[int(self.num_pages*(self._page -1)):int(self.num_pages*(self._page-1)+self.num_pages)]})()
			def __iter__(self):
				return self
			def __next__(self):
				return items.__next__()
		return Pagination()
	@classmethod
	def data(cls,request=None):
		"""
		Cuando asenzor este en produccion
		req=requests.get("zerpatechnology.com.ve/asenzor/json/plugins")
		items=req.json()["items"]
		"""
		items=[{"download":"https://zerpatechnology.com.ve/asenzor/plugins/miplugin",
				"name":"miplugin",
				"id":0,
				"title":"Mi plugin",
				"description":"""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
				tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
				quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
				consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
				cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
				proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
				""",
				"author":"Jesus Zerpa",
				"image":"/static/img/plugin.png"},
				{"download":"https://zerpatechnology.com.ve/asenzor/plugins/miplugin2",
				"name":"miplugin",
				"id":1,
				"title":"Mi plugin2",
				"description":"""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
				tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
				quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
				consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
				cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
				proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
				""",
				"author":"Jesus Zerpa",
				"image":"/static/img/plugin.png"},
				{"download":"https://zerpatechnology.com.ve/asenzor/plugins/miplugin3",
				"name":"miplugin",
				"id":2,
				"title":"Mi plugin3",
				"description":"""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
				tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
				quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
				consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
				cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
				proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
				""",
				"author":"Jesus Zerpa",
				"image":"/static/img/plugin.png"}]
		return {"items":items}
	@classmethod
	def middleware(cls,view,request,data):
		if view=="index":
			items=[]
			print(apps.get_app_config('asenzor').get_plugins())
			for elem in apps.get_app_config('asenzor').plugins:
				items.append({
					"name":elem[0].__name__,
					"title":elem[0].__title__,
					"autores":elem[0].__authors__,
					"version":elem[0].__version__,
					"description":elem[0].__doc__ if elem[0].__doc__ else "",
					})
			data["object_list"]=items
			data["list_display"]=["name","description"]
		elif view=="new":
			data["DATA"]["plugins"]=cls.data()["items"]
	
		

			

@login_required
def customize(request):
	return render(request,"asenzor/layouts/customize.html",locals())

def login(request):
	from django.conf import settings
	from django.contrib.auth import authenticate,login

	if request.method=="POST":

		user = authenticate(
			username=request.POST.get("username"), 
			password=request.POST.get("password"))
		if user:
			request.user=user
	
			login(request, user)
			return HttpResponseRedirect(settings.ASENZOR_URL)
	else:
		return render(request,"asenzor/layouts/login.html",{
			"LOGOUT_REDIRECT_URL":settings.LOGOUT_REDIRECT_URL
			})
@login_required
def builder(request,id=None):
	return render(request,"asenzor/builder.html")
@login_required
def upgrade(request):
	from django.conf import settings
	from django.apps import apps
	asenzor=apps.get_app_config("asenzor")
	import requests,threading
	req=requests.get("https://zerpatechnology/json/version")
	if req.json()["__version__"]!=asenzor.__version__:
		req=requests.get("https://zerpatechnology/asenzor/downloads/asenzor-lastversion.zip")
		
		if not os.path.exists("backups/downloads/"):
			os.mkdir("backups/downloads/")
		with open("backups/downloads/asenzor-lastversion.zip","wb") as f:
			f.write(req.content)
		import zipfile
		ruta_zip = "backups/downloads/asenzor-lastversion.zip"
		ruta_extraccion = ""
		password = None
		archivo_zip = zipfile.ZipFile(ruta_zip, "r")
		try:
		    print(archivo_zip.namelist())
		    archivo_zip.extractall(pwd=password, path=ruta_extraccion)
		except:
		    pass
		archivo_zip.close()
		def asenzor_process():
			os.popen("python manage.py dbbackup")
			os.popen("python manage.py migrate")
			p.stop()
		p=threading.Thread(target=asenzor_process,args=())

		return HttpResponseRedirect(settings.ASENZOR_URL)
	return render(request,"asenzor/layouts/dashboard.html")

def dynamic_views(request):
	"""
	Esta son todas las listas de post con sus guid que posee asenzor
	"""
	from .models import Post,PostMeta,Option,Site
	import hashlib
	multisite=Option.get("multisite",False)
	master=Site.get_master()
	
	
	def findPage(request,model,meta,option,site,multisite=False):

		for elem in model.objects.all():

			if multisite:
				url="/"+site.name+"/"+elem.guid+"/"
			else:
				url="/"+elem.guid+"/"
			

			if request.get_full_path()== url:
				

				authenticated=True
				template=site.name+"/single.html"
				if elem.status=="private":
					if request.method=="POST":
						password=request.POST.get("_post_password")
						users_authenticated=PostMeta.get(elem,"users_authenticated",[])
						print([ hashlib.md5(password.encode("utf-8")).hexdigest() != elem.password, hashlib.md5(password.encode("utf-8")).hexdigest() , elem.password])
						accept=hashlib.md5(password.encode("utf-8")).hexdigest() == elem.password
						if not accept:
							template="asenzor/content-authenticated.html"
							authenticated=False
						elif request.user.is_authenticated and request.user.id not in users_authenticated:
							users_authenticated.append(request.user.id)
							PostMeta.update(elem,"users_authenticated",users_authenticated,True)


					elif request.method=="GET":
						users_authenticated=PostMeta.get(elem,"users_authenticated",[])
						if request.user.is_authenticated:
							print("rrrrrrr",users_authenticated)
							if request.user.id not in users_authenticated:
								template="asenzor/content-authenticated.html"
								authenticated=False
						else:
							template="asenzor/content-authenticated.html"
							authenticated=False

				elif elem.status=="trash" and not request.user.is_authenticated:
					return None
				if authenticated:
					if elem.type=="page":
						template=meta.get(elem.id,"template",site.name+"/single.html")
				print("oooooooooo",template)	
				return {"template":template,"post":elem}

				
	if multisite:
		import imp
		for elem in Site.objects.all():
			if not elem.master and request.get_full_path().startswith(elem.name):
				PostModel=imp.load_from_source("model_"+elem.name,elem.name+"/models.py").Post
				PostModelMeta=imp.load_from_source("model_"+elem.name,elem.name+"/models.py").PostMeta
				OptionModel=imp.load_from_source("model_"+elem.name,elem.name+"/models.py").Option
				data=findPage(request,elem.name+"/"+PostModel.guid,Post,PostModelMeta,OptionModel,elem,True)
				if data:
					template=data["template"]
					if not template:
						template=master.name+"/single.html"
					return render(request,template,{
						"post":data["post"],
						"page":asenzor.get_data_page(data["post"].id),
						"meta":PostModelMeta
						})
			else:
				data=findPage(request,Post,PostMeta,OptionModel,master,True)
				meta={}
				for elem in PostMeta.objects.filter(post=data["post"].id):
					meta[elem.key]=json.loads(elem.value)
				template=data["template"]
				if not template:
					template=master.name+"/single.html"
				if data:
					return render(request,template,{
						"post":data["post"],
						"page":asenzor.get_data_page(data["post"].id),
						"meta":meta
						})

	else:
		data=findPage(request,Post,PostMeta,Option,master)
		if data:
			meta={}
	
			for elem in PostMeta.objects.filter(post=data["post"].id):
				meta[elem.key]=json.loads(elem.value)
			template=data["template"]
			if not template:
				template=master.name+"/single.html"
			return render(request,template,{
				"post":data["post"],
				"page":asenzor.get_data_page(data["post"].id),
				"meta":meta
				})
	return HttpResponse(status=404)

