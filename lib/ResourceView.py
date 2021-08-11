from django.urls import path, include,re_path

from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,multipartparser
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage
from django.forms.models import model_to_dict
from django.db import models
from functools import wraps
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import caches
import json,os
from copy import copy
from datetime import datetime,date,time
from io import BytesIO
from .zgrafic import thumbails

'''
def menu(menu,label,permissions=[],icon=None,to=None,position=-1,styles=None):
    def wrapper(fn):        
        request=get_request()
        user=request.user
        can=True
        def wrapper2(self,request)
        for elem in permissions:
            if not user.user_can(elem):
                can=False
                break
        if can:
            settings.MENUS["ADMIN_MENU"].append([self.slug+])

        return wrapper2
    return wrapper
''' 
class NotCanEdit(Exception):
    """docstring for NotCanEdit"""

def login_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.method=="POST":
            from django.contrib.auth import authenticate,login
            user = authenticate(
                username=request.POST.get("username"), 
                password=request.POST.get("password"))
            if user:
                request.user=user
                login(request, user)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        elif request.method=="GET":
            if not request.user.is_authenticated:  
                return render(request,"asenzor/layouts/login.html")
            else:
                return fn(request,*args,**kwargs)
    return wrapper

    


def admin_menu(label,permissions=[],icon=None):
    return menu("ADMIN_MENU",label,permissions=[],icon=None)
class CachePage:
    def __init__(self,time,fn):
        self.time=time
        self.fn=fn

"""
def cache_page(time):
    def wrapper(fn):        
        
        return CachePage(time,fn)
    return wrapper
"""
def can_edit(cls,field,user):
    """
    Establece si un usario puede editar un campo determinado del modelo
    """
    if "can_edit" in dir(cls._meta):
        for elem in cls._meta.can_edit:
            if elem==field:
                if user.has_perm(cls._meta.can_edit[elem]):
                    return False
    return True

def can_view(cls,field,user):
    """
    Establece si el usuario para ver determinado campo del modelo 
    necesita tener un permiso determinado, de lo contrario este se 
    debera ocultar
    """
    if "_meta" in dir(cls) and  "can_view" in dir(cls._meta):

        for elem in cls._meta.can_view:
            if elem==field:
                if user.has_perm(cls._meta.can_view[elem]):
                    return False
    return True
def clear_view(model,data,user):
    for elem in data.keys():
        if not can_view(model,elem,user):
            del data[elem]
    return data
def cache_page(time):
    from django.views.decorators.cache import cache_page as cache
    def cache_wrapper(fn):
        def wrapper(self,request,*args,**kwargs):
            def wrapper2(request,self,*args,**kwargs):
                return fn(self,request,*args,**kwargs)
            return cache(wrapper2)(request,self,*args,**kwargs)
        return wrapper
    return cache_wrapper


def json_login_required(fn=None,message=None,permissions=[]):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
    if not fn:
        def wrapper(fn):
            def wrapper2(request,*args,**kwargs):
                if request.user.is_authenticated():
                    for elem in permissions:
                        if not  request.user.has_perm(elem):
                            if not message:
                                message="No tienes los permisos necesarios para acceder"
                            return JsonResponse({"_meta":{"message":message}},status=403)
                    return fn(request,*args,**kwargs)
                else:
                    if not message:
                        message="Debes estar autenticado para acceder"
                    return JsonResponse({"_meta":{"message":message}},status=401)
            return wrapper
    return wrapper


def permission_required(fn):
    from django.contrib.auth.decorators import permission_required

        
def serialize(instance,fields=[]):
    serie=model_to_dict(instance)
    for elem in serie:
        if type(serie[elem]) in [
                    models.ForeignKey,
                    models.ManyToManyField 
                ]:

            serie[elem]=model_to_dict(serie[elem])
    if type(serie)==dict:
        keys=list(serie)
        for elem in keys:
            if type(serie[elem])==datetime or type(serie[elem])==date or type(serie[elem])==time:
                serie[elem]=str(serie[elem])
            if fields and elem not in fields:
                del serie[elem]
    return serie

def overwrite(view_manager):
    def wrapper(fn):
        setattr(view_manager,fn.__name__,fn)
    return wrapper


    

class ResourceView(object):
    model=None
    modelMeta=None
    order_by="-id"
    paginator=Paginator
    slug=None
    list_display=None
    btn_new=None
    form_new=None
    form=None
    enable_btn_create=True
    form_new_fields=[]
    subroutes=[]
    btns=[]
    btns_show=[]
    warnings=[]
    filter={}

    actions=[{"label":"Editar","name":"edit","class":"btn"},{"label":"Eliminar","name":"delete","class":"btn red"}]
    

    enable_custom_actions=False
    domain_host=""
    form_fields="__all__"
    form_new_fields="__all__"
    new_redirect="../"
    page_param="page"
    search_param="q"
    search_filter=[]
    json_controller=None
    permissions={}#{method:[permissions]}#los uso aqui ya que puedo indicarle al menu que se coloque si esta aqui
    title=None
    title_new=None
    title_edit=None
    title_show=None
    edit_action=None
    new_action=None
    edit_template="asenzor/widgets/edit.html"
    index_template="asenzor/widgets/table.html"
    show_template="asenzor/widgets/show.html"
    edit_novalidate=False
    new_novalidate=False
    new_template="asenzor/widgets/new.html"
    custom_data={"edit":{},"index":{},"new":{},"delete":{}}

    
    def __init__(self,slug,urlpatterns,name=None):
        self.slug=slug
        if "btns_format" not in dir(self):
            self.btns_format=[]
        if "custom_actions" not in dir(self):
            self.custom_actions=[]#esta pensado apara botones de acciones individuales
        for k,elem in enumerate(self.btns):  

            if len(elem)<3:
                self.btns[k]=list(elem)+["btn "]
            elif len(elem)<4:
                self.btns[k]=list(self.btns[k])
                if elem[2]==None:
                    self.btns[k]+=["btn","get"]
                
                #name,url,class,method

        if self.title==None:
            self.title=self.__class__.__name__
        if self.title_new==None:
            self.title_new="Nuevo "+self.__class__.__name__
        if self.title_edit==None:
            self.title_edit="Editar "+self.__class__.__name__
        if self.title_show==None:
            self.title_show=self.__class__.__name__
        title_new=None
        title_edit=None
        
        for elem in self.subroutes:
            
            if len(elem)==3:
                #route,method,model,post_actions
                def fn(*args,**kwargs):

                    kwargs["model"]=fn.route[2]
                    return getattr(self,fn.route[1])(*args,**kwargs)
                fn.route=elem
                if type(elem[0])==str:
                    urlpatterns.append(path(self.slug+elem[0],fn))
                else:
                    urlpatterns.append(re_path(self.slug+elem[0].pattern,fn))


            if len(elem)==2:
                if type(elem[0])==str:
                    urlpatterns.append(path(self.slug+elem[0],
                        cache_page(getattr(self,elem[1]).time)(lambda request: getattr(self,elem[1]).fn(self,request)) if type(getattr(self,elem[1]))==CachePage else getattr(self,elem[1]))
                        )
                else:
                    urlpatterns.append(re_path(self.slug+elem[0].pattern, 
                            cache_page(getattr(self,elem[1]).time)(lambda request: getattr(self,elem[1]).fn(self,request)) if type(getattr(self,elem[1]))==CachePage else getattr(self,elem[1])))
        """
        def wrapper(request):

            return self.index.fn(self,request)

        urlpatterns.append(path(self.slug,cache_page(self.index.time)(wrapper) if type(self.index)==CachePage else self.index,
                                name=name)
                             )
        if name!=None:
            urlpatterns.append(path(self.slug+"new/",cache_page(self.new.time)(lambda request,**kwargs: self.new.fn(self,request,**kwargs)) if type(self.new)==CachePage else self.new,name=name+"_new"))
            urlpatterns.append(path(self.slug+"<id>/",cache_page(self.show.time)(lambda request,**kwargs: self.show.fn(self,request,**kwargs)) if type(self.show)==CachePage else self.show,name=name+"_show"))
            urlpatterns.append(path(self.slug+"<id>/edit/",cache_page(self.edit.time)(lambda request,**kwargs: self.edit.fn(self,request,**kwargs)) if type(self.edit)==CachePage else self.edit,name=name+"_edit"))
            urlpatterns.append(path(self.slug+"<id>/delete/",cache_page(self.destroy.time)(lambda request,**kwargs: self.destroy.fn(self,request,**kwargs)) if type(self.destroy)==CachePage else self.destroy,name=name+"_destroy"))
            urlpatterns.append(path(self.slug,self.__call__,name=name))
            pass
        """
        
        urlpatterns.append(path(self.slug,self.index,name=name))
        if name!=None:
            urlpatterns.append(path(self.slug+"new/",self.new,name=name+"_new"))
            urlpatterns.append(path(self.slug+"<id>/",self.show,name=name+"_show"))
            urlpatterns.append(path(self.slug+"<id>/edit/",self.edit,name=name+"_edit"))
            urlpatterns.append(path(self.slug+"<id>/delete/",self.destroy,name=name+"_destroy"))
            urlpatterns.append(path(self.slug,self.__call__,name=name))
            pass
    def login_required(self,request):
        from django.contrib.auth.decorators import login_required as login
        from django.conf import settings
        from django.urls import reverse_lazy,reverse
        
        if not request.user.is_authenticated:
            login_view= settings.LOGIN_VIEW if "LOGIN_VIEW" in dir(settings) else "asenzor/layouts/login.html"
            return render(request,login_view,{"LOGOUT_REDIRECT_URL":settings.LOGOUT_REDIRECT_URL})
                
        
    
    def index(self,request,data={},filters={}):
        """
        muestra la pagina inicio del modulo
        """
        data=copy(data)
        data["DATA"]={}
        
        if "toolbar" not in data:
            data["toolbar"]={
                "btn_media_enabled":False
            }
        filters=copy(filters)
        if self.filter:
            filters.update(self.filter)
        res=self.login_required(request)
        if res:
            return res

        if request.method=="GET":
            try:        
                action=None
                if "index" in self.custom_data:
                    data.update(self.custom_data["index"])
                self.generate_data(request,"table",data,filters=filters)
            except EmptyPage:
                return redirect()
            locals()["title"]=self.title if "title" not in data else data["title"]
            self.middleware("index",request,data)

            return render(request,self.index_template,data)
        
                    

    
    def show(self,request,id,data={}):
        """
        muestra la pagina de edicion del elemento
        """
        res=self.login_required(request)
        data["DATA"]={}

        if res:return res

        instance=self.model.objects.get(id=int(id))
        data["instance"]=instance
        model=model_to_dict(instance)
        meta=[]
        title=self.model.__name__
        btns=self.btns_show
        if self.modelMeta:
            obj=self.modelMeta._meta.get_fields()
          
            for item in self.modelMeta.objects.filter(**{obj[1].name:instance}):
                meta.append(item)
        
        else:
            meta=[]
        if "show" in self.custom_data:
            data.update(self.custom_data["show"])

        self.middleware("show",request,data,id)
        item=[]
        slug=self.slug
        for key in model:
            item.append((key,model[key]))
        data["item"]=item

        data["title"]=self.title_show if "title" not in data else data["title"]
        return render(request,self.show_template,data)
    
    def edit(self,request,id,methods=["POST","GET"],model=None,actions=[],data={}):
        """
        muestra mensaje de confirmacion de la accion actualizar/elimiar
        """
        res=self.login_required(request)
       
        data["DATA"]={}

        if res:return res

        if request.method=="POST" and request.method in methods:
            
            self.generate_data(request,"edit",locals(),model=model)

            locals()["form"]=locals()["form"](None,request.POST,request.FILES,instance=locals()["item"])
            d={}
            if not self.edit_novalidate and locals()["form"].is_valid():

                locals()["form"].save()

                for action in actions:
                    action.send(request)
                d["status"]=""
                d["status_message"]=""
            else:
                d["status"]=""
                d["status_message"]=""

                #return HttpResponseRedirect("../")
            d=data 
            d["instance"]=locals()["item"]
            d.update(self.custom_data["edit"])
            d["novalidate"]=self.edit_novalidate
            
            d.update(locals())
            self.middleware("edit",request,d,id)
            return render(request,self.edit_template,d)
        elif request.method=="GET"  and request.method in methods:

            self.generate_data(request,"edit",locals(),model=model)
            locals()["title"]=self.title_edit if "title" not in data else data["title"]
            
            locals()["form"]=locals()["form"](request,instance=locals()["item"])
            d=data 
            d["instance"]=locals()["item"]
            d["action"]=self.edit_action

            d["novalidate"]=self.edit_novalidate
            d.update(self.custom_data["edit"])
            d.update(locals())
            self.middleware("edit",request,d,id)

            return render(request,self.edit_template,d)
        

    def create(self,request):
        """
        methodo para crear un nuevo elemento
        """
        return HttpResponse("Debe implementar el metodo 'create'")
  
    def new(self,request,methods=["POST","GET"],model=None,actions=[],data={},choices={}):
        """
        muestra mensaje de confirmacion de la accion actualizar/elimiar
        """
        res=self.login_required(request)
        data["DATA"]={}
        if not self.new_redirect:
            self.new_redirect="../"
        if res:return res
        
        if request.method=="POST" and request.method in methods:
            
            self.generate_data(request,"new",locals(),model=model,choices=choices)
            
            locals()["form"]=locals()["form"](None,request.POST,request.FILES)
          
            d=data
            if locals()["form"].is_valid():

                instance=locals()["form"].save()
                d["instance"]=instance
                for action in actions:
                    action.send(request,object=instance)
                self.middleware("new",request,d)
                return HttpResponseRedirect(self.new_redirect)
            else:
                d["action"]=self.new_action 
                
                d["novalidate"]=self.new_novalidate
                d.update(self.custom_data["new"])
                d.update(locals())
                self.middleware("new",request,d)
                return render(request,self.new_template,d)
        elif request.method=="GET"  and request.method in methods:
            locals()["title"]=self.title_new if "title" not in data else data["title"]
            self.generate_data(request,"new",locals(),model=model,choices=choices)
            d=data 
            if "new" in self.custom_data:
                d.update(self.custom_data["new"])
            
            d.update(locals())
            self.middleware("new",request,d)
            return render(request,self.new_template,d)


    def update(self):
        """
        methodo para actualizar
        """
        return HttpResponse("Debe implementar el metodo 'update'")

    def destroy(self,request,id,methods=["POST","GET"],model=None,actions=[]):
        """
        muestra mensaje de confirmacion de la accion actualizar/elimiar
        """
        res=self.login_required(request)
        
        if res:return res

        if model==None:
            model=self.model
        if request.method=="POST" and request.method in methods:
            if request.POST.get("delete")=="delete":
                item=model.objects.get(id=int(id))
                item.delete()
                for action in actions:
                    action.send(request)
                return HttpResponseRedirect("../../")
            
        elif request.method=="GET"  and request.method in methods:
            item=model.objects.get(id=int(id))
            
            
            return render(request,"asenzor/widgets/delete.html",locals())

    def paginate(self,request,pagination,model=None,filters={}):
        if model==None:
            model=self.model
        queryset=None

        if self.search_filter:
            search=request.GET.get(self.search_param)
            filters={}
            if ";" in search:#ya con esto se deberia entender que es una busqueda inteligente
                for elem in search.split(";"):

                    k,v=elem.split(":")
                    if k in self.search_filter:
                        filters[k]=v
            else:
                filters[self.search_filter[0]]=search
            if model:
                if queryset:
                    queryset=queryset | model.objects.filter(**filters)
                else:
                    queryset=model.objects.filter(**{elem:request.GET.get(self.search_param)})
            else:
                data=self.data(request)
                if "items" in data:
                   items=list(filter(
                    lambda item: all([
                        item[field]==filters[field] for field in filters
                        ]),
                    data["items"]
                    ))
                   return self.paginator(items,pagination)
                else:
                    raise Exception("El metodo data debe tener un parametro items")


        
        else:
            if model:

                queryset=model.objects.filter(**filters)
            else:
                data=self.data(request)
                if "items" in data:
                   queryset=list(filter(
                    lambda item: all([
                        item[field]==filters[field] for field in filters
                        ]),
                    data["items"]
                    ))
                else:
                    raise Exception("El metodo data debe tener un parametro items")
        """
        elif queryset==None or (queryset!=None and len(queryset)==0):            
            queryset=model.objects.filter(**filters).order_by(self.order_by)
        """
        
        object_list=self.paginator(queryset,pagination)
        """
        if len(queryset)>pagination:

            object_list=self.paginator(queryset,pagination)
            
            if "page" in request.GET:
                return object_list.page(int(request.GET.get(self.page_param))).object_list


            return object_list.page(1).object_list
        """
        
        return object_list
    def generate_redirect_paginate(self,request,slug=""):
        return settings.BASE_URL+self.slug+slug+"?"+self.page_param+"=1"+"&"+self.url_params(request)

    def get_page(self,request,object_list,page=None):
        """
        encuentra la pagina de una paginacion
        """
        if type(page)==int:
            return object_list.page(page).object_list
        else:
            if self.page_param in request.GET:
                return object_list.page(int(request.GET.get(self.page_param))).object_list

            else:
                return object_list.page(1).object_list

    def get_paginator(self,request,pagination):
        return self.paginator(self.model.objects.all().order_by(self.order_by),pagination)
    def url_params(self,request):
        import urllib.parse
        params=dict(request.GET)
        if  self.page_param in params:
            del params[self.page_param]
        url_params=urllib.parse.urlencode(params)
        return url_params
        
    def generate_data(self,request,template_type,data,pagination=20,model=None,filters={},exclude=[],choices={}):
        from django.conf import settings

        if model==None:
            model=self.model
        if model==None:
            print(f"El controlador de vista '{self.__class__.__name__}' necesita un modelo")

        if self.btn_new==None and model!=None:
            btn_new="Crear nuevo "+model.__name__
        else:
            btn_new=self.btn_new

        

        if template_type=="table":
           

            if self.list_display==None and model!=None:
                list_display=[]
                for field in model._meta.get_fields():
                    if "verbose_name" in dir(field) and "value_from_object"in dir(field) :
                        list_display.append(field.name)
    
                
                list_display.remove("id")

            else:
                list_display=self.list_display

            url_params=self.url_params(request)

            object_list=self.paginate(request,pagination,model=model,filters=filters)
            num_pages=object_list.num_pages
            #EmptyPage
            object_list=self.get_page(request,object_list)
            
            
            self.custom_actions=[]
            btns_format=[]

            
            for item in  object_list:
                
                if item:
                    if self.enable_custom_actions:
                        self.custom_actions.append(item.actions)
                    
                    data["item"]=item
                    btns=[]
                    for btn in self.btns_format if "btns_format" not in data else data["btns_format"]:
                        btns.append({"label":btn["label"],"url":btn["url"].format(**data),"class":btn["class"], "type": btn["type"] if "type" in btn else None})
                    btns_format.append(btns)
            



                else:
                    if self.enable_custom_actions:
                        self.custom_actions.append(None)
            page_before=None
            page_next=None
            if "json_controller" not in data and self.json_controller:
                data["json_controller"]=settings.BASE_URL+self.json_controller

            page_current=1
            if self.page_param in request.GET.keys():
                page_current=int(request.GET.get(self.page_param))
           
            data.update({"object_list":object_list,
                         "list_display":list_display if "list_display" not in data else data["list_display"],
                         "model":model,
                         "btn_new":btn_new,
                         "base_slug":settings.BASE_URL+self.slug if "slug" not in data else settings.BASE_URL+data["slug"],
                         "btns":self.btns,
                         "page_param":self.page_param,
                         "btnsformat":btns_format,
                         "num_pages":range(1,num_pages+1),
                         "enable_btn_create":self.enable_btn_create,
                         "actions":self.actions,
                         "custom_actions":self.custom_actions,
                         "page_current":page_current,
                         "page_next":page_next,
                         "page_before":page_before,
                         "url_params":url_params})
            if exclude:
                for elem in exclude:
                    i=data["list_display"].index(elem)
                    del data["list_display"][i]
        elif template_type=="new":
            

            if self.form_new==None and "form" not in data:
                
                from django.forms import ModelForm
                from django import forms
                
                from asenzor.forms import TemplateModelForm
                _model=model
                if model:
                    class Form(TemplateModelForm):
                        def __init__(self,request=None,*args,**kwargs):
                            super(Form,self).__init__(*args,**kwargs)
                            for choice in choices:
                                self.fields[choice]=forms.ChoiceField(choices=choices[choice],label=self.fields[choice].label)
                            
                        class Meta:
                            model = _model
                            fields=self.form_new_fields
                        
                    if request.method=="GET":
                        _form=Form(request)
                    elif request.method=="POST":
                        _form=Form
                else:
                    _form=None
                
            elif "form" in data:
                _form=data["form"]
            else:
               
                _form=self.form_new
            
            data.update({"form":_form,
                     "btn_new":btn_new,
                     "base_slug":self.domain_host+self.slug,
                     "enable_btn_create":self.enable_btn_create})

        elif template_type=="edit": 

            item=model.objects.get(id=int(data["id"]))


            
            if self.form==None:
                from django.forms import ModelForm
                from django import forms
                
                from asenzor.forms import TemplateModelForm
                _model=model
                class Form(TemplateModelForm):
                    def __init__(self,request=None,*args,**kwargs):
                        super(Form,self).__init__(*args,**kwargs)
                        
                    class Meta:
                        model = _model
                        fields=self.form_new_fields                
                
                _form=Form

                

            else:
                
                
                _form=self.form
            
            data.update({"form":_form,
                 "btn_new":btn_new,
                 "base_slug":self.domain_host+self.slug,
                 "enable_btn_create":self.enable_btn_create,
                 "item":item,
                 "x":2
                 })
        #data.update({"BASE_URL":settings.BASE_URL})
        return 

    def set_warning(self,request,message,style=".alert .alert-warning",keep=False):
        self.warnings.append([request.user.id,message,style,keep])
    def get_warnings(self,request):
        warnings=[]
        _warnings=self.warnings
        for k,elem in enumerate(_warnings):
            if request.user.id==elem[0]:
                warnings.append([elem[2],elem[1]])
                if not elem[3]:
                    del self.warnings[k]      
        return warnings
    @classmethod
    def middleware(cls,view,request,data,id=None):
        pass
    @classmethod
    def data(cls,request=None):
        return {"items":[]}





        
            
        
    def __call__(self,request,id=None,method=None):
        return render(request,"404.html",locals())
        """
        _path=request.path.split("/")
        path=[]
    
        for elem in _path:
            if elem:
                path.append(elem)




        if request.method=="POST":
            return self.create(request)
        elif request.method=="GET":
            
            if request.path=="/"+self.slug:
                return self.index(request)

            elif len(path)==3 and path[0]==self.slug[:-1] and path[1].isdigit() and path[2]=="edit":

                return self.edit(request,id)
            elif len(path)==2 and path[0]==self.slug[:-1] and path[1].isdigit():
                return self.show(request,id)

        elif request.method=="PUT":
            if method!=None:
                return self.update(request,id)
            else:
                return self.update(request,id)
        elif request.method=="DELETE":
            if id!=None:
                return self.destroy(request,id)
        return HttpResponse("default")
        """
    

class ResourceViewRest(ResourceView):
    csrf_exempt=csrf_exempt
    permissions={"get":[],
                 "post":[],
                 "search":[],
                 "patch":[]}
    upload_path=None

    def __init__(self,slug,urlpatterns,name=None):
        self.slug=slug
        if not self.slug.endswith("/"):
            print(self.slug," debe terminar con un / porfavor corrija")

        for elem in self.subroutes:
            if len(elem)>2:

                urlpatterns.append(path(self.slug+elem[0],getattr(self,elem[1]),name=elem[2]))
            else:

                urlpatterns.append(path(self.slug+elem[0],csrf_exempt(getattr(self,elem[1]) )))


        urlpatterns.append(path(self.slug,self.api,name=name))
        urlpatterns.append(path(self.slug+"<id>/",self.api,name=name))
        
        #urlpatterns.append(path(slug,self.__call__,name=name))
    def login_required(self,request,message=None,permissions=[]):
        request.user=self.basic_auth(request)
        if request.user.is_authenticated:
            for elem in permissions:
                if not  request.user.has_perm(elem):
                    if not message:
                        message="No tienes los permisos necesarios para acceder"
                    return JsonResponse({"_meta":{"message":message}},status=403)
        else:

            if not message:
                message="Debes estar autenticado para acceder"
            return JsonResponse({"_meta":{"message":message}},status=401)


    def basic_auth(self,request):
        import base64
        from django.contrib.auth import authenticate
        if hasattr(request, "user") and request.user.is_authenticated:
            return  request.user# Don't interfere with standard authentication

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
        
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    
                    uname, passwd = base64.b64decode(auth[1]).decode("utf-8").split(':')
                    user = authenticate(username=uname, password=passwd)
                    return user
    def token_auth(self,request):
        if hasattr(request, "user") and request.user.is_authenticated:
            return  request.user# Don't interfere with standard authentication
        else:
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
        
                if len(auth) == 2:
                    if auth[0].lower() == "token":
                        meta=UserMeta.objects.get("token",auth[1].decode("utf-8"))
                        return meta.user




    def parse_formdata(self,request):
        if request.content_type == 'multipart/form-data':
            if hasattr(request, '_body'):
                # Use already read data
                data = BytesIO(request._body)
            else:
                data = request
            
            try:
                #_post, _files = request.parse_file_upload(request.META, data)
                parser=multipartparser.MultiPartParser(request.META,data,request.upload_handlers, request.encoding)
                _post, request._files =parser.parse()
                if request.method=="PATCH":
                    request.PATCH=_post
                elif request.method=="PUT":
                    request.PUT=_post
                elif request.method=="DELETE":
                    request.DELETE=_post
            except Exception as e:
                raise  e
    @csrf_exempt
    def api(self,request,id=None):
        print("######",request.method)
        if request.method=="GET" and id:
            return self.get(request,id)
        if request.method=="GET":
            return self.search(request)
        elif request.method=="POST":
            return self.post(request)
        elif request.method=="PUT":
            self.parse_formdata(request)
            return self.put(request,id)
        elif request.method=="PATCH":
            self.parse_formdata(request)
            return self.patch(request,id)
        elif request.method=="DELETE" and id:
            return self.delete(request,id)
    def search(self,request,filters={}):
        if self.model:
            
            data={k:v for k,v in request.GET.items()}
           
            filters.update(self.filter)
            data.update(filters)
            items=[clear_view(self.model,serialize(item),request.user) for item in self.model.objects.filter(**data)]
            data["items"]=items
            
            self.middleware("search",request,data)
            return JsonResponse({
                "_meta":{"message":f"{len(items)} resultados"},
                "items":items})

    def get(self,request,id):
        """
        muestra la pagina inicio del modulo
        """
        if self.model:
            try:
                data={key:value for key,value in request.GET.items()}
                data["id"]=id
                data["item"]=clear_view(self.model,serialize(self.model.objects.get(**data)),request.user )

                self.middleware("get",request,data)

                return JsonResponse({"_meta":{"message":"Busqueda encontrada"},"item":data["item"]})
            except Exception as e:
             
                return JsonResponse({"_meta":{"message":"No se encontraron resultados","item":None}})
        return HttpResponse("Debe implementar el metodo 'index'")
    
    def post(self,request):
        """
        muestra la pagina de edicion del elemento
        """
        res=self.login_required(request)
        if res:return res
        
        if self.model:
            if request.body:
              
                if request.headers["Content-Type"]=="application/json":
                    data=json.loads(request.body)  
                else:
                    data={key:value for key,value in request.POST.items()}
                
                if self.model:
                    for elem in self.model._meta.get_fields():
                        if elem.name in data:
                            if type(elem)==models.ForeignKey and data[elem.name]!=None:
                                item=data[elem.name]
                                data[elem.name]=elem.related_model.objects.get(id=item)
                            elif type(elem)==models.ManyToManyField and data[elem.name]!=None:
                                items=data[elem.name]
                                l=[]
                                for i in items:
                                    l.append(elem.related_model.objects.get(id=i))
                                data[elem.name]=l    
                            elif data[elem.name]==None:
                                del data[elem.name] 

                if request.FILES:
                    files=self.upload(request,data)

                    data=self.uploaded(request,data,files)
                if self.model:
                    is_post=False
                    for elem in self.model._meta.get_fields():
                        if elem.name=="guid":
                            is_post=True
                            break
                    if is_post:
                        name=None
                        if "name" not in data and "title" in data:
                            name=data["title"].lower()
                        elif "name" in data:
                            name=data["name"]
                        newname=name
                        newname.replace(" ","-")
                        c=1
                        while True:
                            try:
                                self.model.objects.get(name=newname)
                                newname=name+f"-{c}"
                                c+=1
                            except Exception as e:
                                break
                    
                        data["name"]=newname
                        data["guid"]=newname
                        instance=self.model.objects.create(**data)
                        #instance.save()
                        data["item"]=clear_view(self.model,serialize(instance),request.user)
                    else:
                        instance=self.model.objects.create(**data)
                        data["item"]=clear_view(self.model,serialize(instance),request.user)

                    self.middleware("post",request,data)

                    return JsonResponse({"_meta":{"message":str(instance)+" Creada con exito"},"item":data["item"]})

            else:
                return JsonResponse({"_meta":{"message":" No se proporcionaron los datos para crear el registro"},"item":None})
    
        return HttpResponse("Debe implementar el metodo 'show'")
    def put(self,request,id=None,):
        """
        muestra mensaje de confirmacion de la accion actualizar/elimiar
        """
        res=self.login_required(request)
        if res:return res

        if self.model:
            instance=self.model.objects.get(id=id)
            if request.headers["Content-Type"]=="application/json":
                    data=json.loads(request.body)  
            else:
                data={key:value for key,value in request.PUT.items()}
            if id==None:
                id=data["id"]
            self.middleware("put",request,data)
            for elem in self.model._meta.get_fields():
                if elem.name in data:
                    if type(elem)==models.ForeignKey and data[elem.name]!=None:
                        item=data[elem.name]
                        data[elem.name]=elem.related_model.objects.get(id=item)
                    elif type(elem)==models.ManyToManyField and data[elem.name]!=None:
                        items=data[elem.name]
                        l=[]
                        for i in items:
                            l.append(elem.related_model.objects.get(id=i))
                        data[elem.name]=l     
            for elem in data:
           
                if can_edit(self.model,elem,request.user):
                    setattr(instance,elem,data[elem])
                    
                else:
                    raise NotCanEdit(elem)
            instance.save()
            return JsonResponse({"_meta":{"message":f"{instance} actualizada con exito"},"item":clear_view(self.model,serialize(instance),request.user )})
        return HttpResponse("Debe implementar el metodo 'edit'")
    
    def patch(self,request,id=None):
        """
        methodo para crear un nuevo elemento
        """
     
        res=self.login_required(request)
        if res:return res

        if self.model:
            if request.headers["Content-Type"]=="application/json":
                data=json.loads(request.body)
            else:
                data={key:value for key,value in request.PATCH.items()}
            if id==None:
                id=int(data["id"])
            instance=self.model.objects.get(id=id)
            self.middleware("patch",request,data)
            for elem in self.model._meta.get_fields():
                if elem.name in data:
                    if type(elem)==models.ForeignKey and data[elem.name]!=None:
                        item=data[elem.name]

                        data[elem.name]=elem.related_model.objects.get(id=item)
                    elif type(elem)==models.ManyToManyField and data[elem.name]!=None:
                        items=data[elem.name]
                        l=[]
                        for i in items:
                            l.append(elem.related_model.objects.get(id=i))
                        data[elem.name]=l  
            
            for elem in data:
           
                if can_edit(self.model,elem,request.user):
                    setattr(instance,elem,data[elem])
                    
                else:
                    raise NotCanEdit(elem)
            instance.save()
            return JsonResponse({"_meta":{"message":f"{instance} actualizada con exito"},"item":clear_view(self.model,serialize(instance),request.user)})

        return HttpResponse("Debe implementar el metodo 'create'")
    def delete(self,request,id=None):
        """
        methodo para actualizar
        """
        res=self.login_required(request)
        if res:return res

        if self.model:
            if request.headers["Content-Type"]=="application/json":
                data=json.loads(request.body)
            else:
                data={key:value for key,value in request.DELETE.items()}
            if id==None:
                id=data["id"]
            instance=self.model.objects.get(id=id)
            instance.delete()
            return JsonResponse({"_meta":{"message":f"{id} Eliminado con exito"},"item":id})

        return HttpResponse("Debe implementar el metodo 'update'")
    def upload(self,request,data):
        datedir=datetime.now().strftime("%Y/%m/%d/")
        if not self.upload_path:
            path='media/'+datedir
        else:
            path=self.upload_path
        if not os.path.exists(path):
            os.makedirs(path,exist_ok=True)
        
        files=[]
        for file in request.FILES:
            name,ext=os.path.splitext(request.FILES[file].name)
            
            data=self.handle_uploaded_file(path,request.FILES[file])
        
            files.append({"name":datedir+data["name"],"url":datedir+data["name"],"mime_type":data["mime_type"]}) 
        
        if len(files)>1:
            return files
        else:
            return files[0]
    def middleware(self,view,request,data):
        pass
   
    def uploaded(self,request,data,files):
        if files:      
            if type(files)==list:
                url=",".join([file["url"] for file in files])
                name=f"Multiples Files nª:{len(files)}"
            else:
                url=files["url"]
                name=files["name"]
            data["name"]=name
            data["guid"]=url
            data["type"]="attachment"
            data["mime_type"]=files["mime_type"]
         
        else:
            if "type" not in data:
                data["type"]="post"
        data["author"]=request.user
        

        return data
    
    def handle_uploaded_file(self,path,file):
        name,ext=os.path.splitext(file.name)
        new_name=name.replace(" ","-")+ext
        fullname=path+name.replace(" ","-")+ext
        c=0
        if ext.lower() in [".jpg",".png",".jpeg",".gif",".bmp",".svg"]:
            mime_type="image/"+ext[1:]

        while os.path.exists(fullname):
            new_name=name.replace(" ","-")+f"({c})"+ext
            fullname=path+new_name
            c+=1
        with open(fullname, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        thumbails(new_name,sufijo="_600-600",alto=600,ancho=600,path=path)
        thumbails(new_name,sufijo="_300-300",alto=300,ancho=300,path=path)
        thumbails(new_name,sufijo="_150-150",alto=150,ancho=150,path=path)
        return {"name":new_name,"mime_type":mime_type}

    
    def __call__(self,request,id=None,method=None):
        """
        if request.method=="POST":
            return self.create(request)
        elif request.method=="GET":
            if id==None:
                return self.index(request)
            elif method==None:
                return self.edit(request,id)
            else:
                return self.show(request,id)

        elif request.method=="PUT":
            if method!=None:
                return self.update(request,id)
            else:
                return self.update(request,id)
        elif request.method=="DELETE":
            if id!=None:
                return self.destroy(request,id)
        return HttpResponse("default")
        """
    
    



    
        
