from django.db import models
from django.contrib.auth.models import User, Group,Permission
from datetime import datetime
from django.utils import timezone
import jsonfield,json

# Create your models here.
class Form(models.Model):
	"""docstring for Forms"""
	name=models.CharField(max_length=250)
	fields=jsonfield.JSONField(default=[])
	def add_field(self,label,name,type,default,**kwargs):
		fields=this.fields
		types=["InputText","TinyMCE","Select"]
		if type in types:
			field={"label":label,
						   "type":type,
						   "name":name,
						   "default":default}
			fields.append(field)
		else:
			raise Exception(f"El {type} es un tipo desconocido")
			
			
		
class Post(models.Model):
	"""docstring for Forms"""
	TYPE=[("post","Entrada"),
		  ("page","Pagina"),
		  ("form","Formulario"),
		  ("attachment","Medio"),
		  ]
	name=models.CharField("Nombre",max_length=250,unique=True)
	type=models.CharField("Tipo",max_length=250,choices=TYPE,blank=False,null=False)
	author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
	date=models.DateField(default=datetime.now)
	content=models.TextField(null=True,blank=True)
	title=models.CharField("Titulo",max_length=250,null=True,blank=True)
	excerpt=models.TextField(null=True,blank=True)
	status=models.CharField("Estatus",max_length=250,null=True,blank=True)
	comment_status=models.CharField(max_length=250,null=True,blank=True)
	ping_status=models.CharField(max_length=250,null=True,blank=True)
	password=models.CharField(max_length=250,null=True,blank=True)
	modified=models.DateTimeField(max_length=250,default= timezone.now)
	content_filtered=models.TextField(max_length=250,blank=True,null=True)
	parent=models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True)
	guid=models.CharField(max_length=250,unique=True)
	menu_order=models.IntegerField(null=True,blank=True,default=0)
	mime_type=models.CharField(max_length=250,blank=True,null=True)
	comment_count=models.IntegerField(null=True,blank=True,default=0)
	def __str__(self):
		return f"Post[{self.id}]:{self.type}:{self.name}"



class PostMeta(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	key=models.CharField(max_length=250)
	value=models.TextField()
	encrypted=models.BooleanField(default=False)
	description=models.TextField(blank=True,null=True,
		help_text="""Este campo sera util para cuando se definen los metadatos
		de forma personalizada, ya que asi tenemos una descripcion rapida para 
		que puede servir si se nos olvida""")
	def __str__(self):
		return f"PostMeta[{self.id}]:{self.key}:{self.value}"
	@classmethod
	def get(cls,id,key,default=None):
		try:
			instance=cls.objects.get(post=id,key=key)
			value=instance.value
			if instance.encrypted and value:
				from django.apps import apps
				asenzor=apps.get_app_config("asenzor")
				value= asenzor.decode(instance.value,ansenzor.get_secret_key())

			if value:
				value=json.loads(value)
			return value
		except Exception as e:
			print(e)
			return default
	@classmethod
	def filter(cls,id,key):
		return [json.loads(elem) for elem in cls.objects.filter(post=id,key=key)]
	@classmethod		
	def set(cls,id,key,value,encrypted):
		if encrypted:
			from django.apps import apps
			asenzor=apps.get_app_config("asenzor")
			value=asenzor.endecode(value,ansenzor.get_secret_key())
		try:
			instance=cls.objects.get(post=id,key=key)
			instance[key]=value
		except:
			instance=cls.objects.create(post=id,key=key,value=value)

	@classmethod
	def update(cls,id,key,value):
		"""

		"""
		query=cls.objects.filter(post=id,key=key)
		l=[]
		if type(value)==list or type(value)==tuple:
			if len(query):

				for k,elem in enumerate(query):
					elem[key]=value[k]
					l.append(elem.id)
			else:
				for elem in value:

					instance=cls.objects.create(post=id,key=key,value=json.dumps(elem))

					l.append(instance.id)


		else:
			if len(query):
				
				setattr(query[0],key,json.dumps(value))
				query[0].save()
				l.append(query[0].id)
			else:
				instance=cls.objects.create(post=id,key=key,value=json.dumps(value))
				l.append(instance.id)

		return l


			



class UserMeta(models.Model):
	"""docstring for Usermeta"""
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	key=models.CharField(max_length=250)
	value=models.TextField()
	encrypted=models.BooleanField(default=False)
	unique=models.BooleanField(default=False)
	description=models.TextField(blank=True,null=True,
		help_text="""Este campo sera util para cuando se definen los metadatos
		de forma personalizada, ya que asi tenemos una descripcion rapida para 
		que puede servir si se nos olvida""")
	@classmethod
	def get(cls,key,default=None):
	
		from django.apps import apps
	
		try:
			instance=cls.objects.get(name=key)
			if instance.encrypted:
				asenzor=apps.get_app_config("asenzor")
				return asenzor.decode(instance.value,ansenzor.get_secret_key())
			else:
				return instance.value
		except Exception as e:
			return default
	@classmethod		
	def update(cls,user,key,value,encrypted=False,unique=False):
		if encrypted:
			from django.apps import apps
			asenzor=apps.get_app_config("asenzor")
			value=asenzor.encode(value,ansenzor.get_secret_key())
		try:

			instance=cls.objects.get(name=key,user=user)
			if instance.user==user:
				setattr(instance,key,value)
				setattr(instance,"unique",unique)
				instance.save()
			elif instance.unique==False:
				raise Exception("No se encontro el registro, se procede a crearlo")
			

		except:
			instance=cls.objects.create(user=user,name=key,value=value,encrypted=encrypted)
			instance.save()
			return instance


class Comment(models.Model):
	"""docstring for Usermeta"""
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	author=models.CharField(max_length=250)
	email=models.CharField(max_length=250)
	url=models.CharField(max_length=250)
	ip=models.CharField(max_length=250)
	date=models.DateField()
	content=models.TextField()
	karma=models.IntegerField()
	approved=models.CharField(max_length=250)
	agent=models.CharField(max_length=250)
	type=models.CharField(max_length=250)
	parent=models.ForeignKey("self",on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
class CommentMeta(models.Model):
	"""docstring for Usermeta"""
	comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
	key=models.CharField(max_length=250)
	value=models.TextField()

		

class Term(models.Model):
	"""docstring for Usermeta"""
	name=models.CharField(max_length=250)
	slug=models.CharField(max_length=250)
	group=models.IntegerField()

class TermTaxonomy(models.Model):
	"""docstring for TermTaxonomy"""
	term=models.ForeignKey(Term,on_delete=models.CASCADE)
	taxonomy=models.CharField(max_length=250)
	description=models.TextField()
	parent=models.ForeignKey("self",on_delete=models.CASCADE)
	count=models.IntegerField()

class Site(models.Model):
	"""docstring for Site"""
	name=models.CharField(max_length=250)
	domain=models.CharField(max_length=250)
	description=models.TextField()
	master=models.BooleanField(unique=True,null=True)
	@classmethod
	def get_master(cls):
		for elem in cls.objects.all():
			if elem.master:return elem
		else:
			if cls.objects.all():
				cls.objects.all()[0].master=1
				cls.objects.all()[0].save()
				return cls.objects.all()[0]
	@classmethod
	def update_master(cls,site):
		if type(site)==int:
			site=cls.objects.get(id=site)
		for elem in cls.objects.all():
			elem.master=None
		site.master=True
	def __str__(self):
		return self.name
		
class Option(models.Model):
	"""docstring for Usermeta"""
	site=models.ForeignKey(Site,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=250,unique=True)
	value=models.TextField()
	autoload=models.CharField(max_length=250,blank=True,null=True)
	encrypted=models.BooleanField(default=False)
	description=models.TextField(blank=True,null=True,
		help_text="""Este campo sera util para cuando se definen las opciones
		de forma personalizada, ya que asi tenemos una descripcion rapida para 
		que puede servir si se nos olvida""")
	@classmethod
	def get(cls,key,default=None,site=None):
		try:
			
			if site!=None:
				
				if type(site)==int:
					site=Site.objects.get(id=site)

				return cls.objects.get(name=key,site=site).value
			else:
				site=Site.get_master()
			
				instance=cls.objects.get(name=key,site=site)
				
				if instance.encrypted:
					from django.apps import apps
					asenzor=apps.get_app_config("asenzor")
				
					return asenzor.decode(instance.value,asenzor.get_secret_key())
				else:
					return instance.value
		except Exception as e:
			print(e)
			return default
	@classmethod		
	def update(cls,key,value,site=None,encrypted=False):
		if encrypted:
			from django.apps import apps
			asenzor=apps.get_app_config("asenzor")
			value=asenzor.encode(value,ansenzor.get_secret_key())
		try:
			if site==None:
				site=Site.get_master()
			print("eeeeeeeee",value)
			instance=cls.objects.get(name=key,site=site,encrypted=encrypted)
			setattr(instance,key,value)
			

		except :
			if type(site)==int:
				site=Site.objects.get(id=site)
			elif site==None:
				site=Site.get_master()
			instance=cls.objects.create(name=key,value=value,encrypted=encrypted)
			instance.save()
			return instance




class Link(models.Model):
	url=models.CharField(max_length=250)
	image=models.CharField(max_length=250)
	target=models.CharField(max_length=250)
	description=models.TextField()
	visible=models.CharField(max_length=250)
	owner=models.ForeignKey(User,on_delete=models.CASCADE)
	raiting=models.IntegerField()
	updated=models.DateTimeField()
	rel=models.CharField(max_length=250)
	notes=models.TextField()
	rss=models.CharField(max_length=250)


class App(models.Model):
	"""
	Esta pensada para controlar las interacciones de otras plataformas
	con esta, gestionar sus permisos y otras cosas
	"""
	name=models.CharField(max_length=250)
	author=models.CharField(max_length=250)
	url=models.CharField(max_length=250)
	user=models.ForeignKey(User,
		on_delete=models.CASCADE,
		help_text="Usuario que sera usado dedicado a la app para manaejar el acceso")