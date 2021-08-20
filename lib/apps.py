from django.apps import AppConfig
from django.conf import settings
import os,json,threading,time,subprocess,sys
from datetime import datetime,timedelta
from copy import copy
from uuid import uuid4
import subprocess
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re,shutil
from pathlib import Path
def watchdog_plugin(sender, **kwargs):
    watch = sender.extra_files.add
    
    for root, dirs, files in os.walk("asenzor/plugins/"):
        for name in files:
            file=os.path.join(root, name)
            if file.endswith(".py"):
                watch(Path(file))

                
    # to listen to multiple files, use watch_dir, e.g.
    # sender.watch_dir('/tmp/', '*.bar')

def compile_webpack(name,path):
    pattern=name+"/static/"+name+r"/py/(\w+)/"

    folder=re.findall(name+"/static/"+name+r"/py/(\w+)",path)[0]
    if os.path.exists(name+"/static/"+name+"/py/"+folder+"/webpack.dev.js"):
        print("compilando webpack...",name,path)

        import subprocess
        proc = subprocess.Popen(
            ["npx","webpack","--config","webpack.dev.js"],
            stdout=subprocess.PIPE,
            cwd=name+"/static/"+name+"/py/"+folder
        )
        print(proc.communicate()[0].decode("utf-8"))
        shutil.move(name+"/static/"+name+"/py/"+folder+"/dist/main.js", name+"/static/"+name+"/dist/"+folder+".js")
        return proc

class MyEventHandler(FileSystemEventHandler):
    def __init__(self,app):
        self.app=app
    def on_modified(self, event):
        #esto porque tambien se registra la modificacion de la carpeta
        if event.src_path.endswith(".py"):
            compile_webpack(self.app,event.src_path)

        print(event.src_path, "modificado.")


def get_process():
    proc = subprocess.Popen(
                ['ps -h'],
                shell=True,
                stdout=subprocess.PIPE,
            )
    stdout_value = proc.communicate()[0].decode('utf-8')
    l=[]
    for line in stdout_value.split("\n")[:-1]:
        l.append(parse_process(line))
    return l

def parse_process(line):
    line=line.strip().split(" ")
    pid=line[0]
    pts=line[1]
    i=None
    f=-1
    for k,elem in enumerate(line[2:]): 
        if elem: 
            break
    ss=line[2+k]
    
    for k2,elem in enumerate(line[2+k+1:]): 
        if elem: 
            
            break

    time=line[2+k+k2+1]
    
    task=" ".join(line[2+k+k2+2:])
    return {"task":task,"time":time,"pts":pts,"pid":pid,"ss":ss}
def search_process(list_process,**kwargs):
    query=["task","ss","pts","pid","time"]
    for elem in kwargs:
        if elem not in query:
            raise Exception(f"El parametro de busqueda '{elem}' es invalido, debe ser alguno de los siguientes:{query}")
    results=[]

    for elem in list_process:
        for param in kwargs:
            if kwargs[param]!=elem[param]:
                break
        else:
            results.append(elem)
    return results
class ValueAttr(json.JSONEncoder):
    def __init__(self,value,name,attrs={}):
        self._value=value
        self.attrs=attrs
        self.name=name
        self._index=0

    def __get__(self):
        return self._value
    def __set__(self,value):
        self._value=value
    """
    def encode_(self, file):
        return json.dumps(self._value)
    """
    def __iter__(self):
        self._index=0
        return self
    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < len(self._value):
            result = self._value[self._index]
            self._index +=1
           
            return result
        # End of Iteration
        raise StopIteration

    def __getitem__(self,k):
        return self._value[k]

        
    def __repr__(self):
        return str(self._value)
    def default(self,o):
        return self._value




templates={}
widgets={}
process=[]

class AppConfig(AppConfig):
    """docstring for """
    not_compile_app=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        ]
    settings={
        "webpack":{
            "entry":{},
            "output":{
                "path":None,
                "filename": "[name].js"
            }
        },
    
    }

    compile=[]
    _checked_block=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if os.path.exists(self.name+'/settings.json'):
            with open(self.name+'/settings.json') as f:
                _settings=f.read()
                if _settings:
                    self.settings=json.loads(_settings)


        self.settings["webpack"]["output"]["path"]=os.path.abspath("./"+self.name+'/static/'+self.name+'/dist/')
        self.loadeds=[]
        self.threads=[]

        from asenzor.signals import app_loaded
        app_loaded.connect(receiver=self.load_requests)
        app_loaded.connect(receiver=self.load_actions)
      
        if self.name in settings.COMPILE_APPS_WEBPACK:
            self.webpack()
        if self.name in settings.COMPILE_APPS_SASS:
            self.sass()    
    
    
    def ready(self):
        super().ready()
        from asenzor.signals import render_started
        from asenzor.signals import app_loaded

        from asenzor.models import CustomPermission,User
    
        render_started.connect(receiver=self.load_menu)
        render_started.connect(receiver=self.load_urls)
        app_loaded.send(sender=self)
        permissions=[]
        try:
            permissions+=[
                CustomPermission.objects.get(codename="admin_log"),
                CustomPermission.objects.get(codename="public_log")
            ]

        except:
            permissions+=[
                CustomPermission.objects.create(
                    codename="admin_log",
                    name="Registros del Administrador"),
                CustomPermission.objects.create(
                    codename="public_log",
                    name="Registros del publicos")
            ]
        for user in User.objects.all():
            if user.is_staff:
                for perm in permissions:
                   
                    if not user.has_perm(perm.codename):
                        
                        user.user_permissions.add(perm)
                user.save()
        



        
    def load_menu(self,sender=None,*args,**kwargs):
        from imp import load_source
        import os
        user=sender.user
        
        def build(menu,item):
            label=item[0]
            url=item[1]
            method=item[2]
            permissions=[]
            if method:
                if type(method)==str:
                    view,method=method.split(".")
                    classview=getattr(__import__(self.label+".views").views,view)
                else:
                    classview=method[0]
                    view=getattr(classview,method[1])
                    method=method[1]
                
                if method in classview.permissions:
                    permissions=classview.permissions[method]
            icon=item[3]
            children=item[4]
            root=item[4] if len(item)>4 else ""
            index=-1
            
            can=True

            if permissions:
                for elem in permissions:
                    if not user.has_perm(elem):
                        can=False
            if can:

                menu.append([url,label,icon,[]])

            for child in children:
                build(menu[3],child)

        if os.path.exists(self.path+"/menus.py") and  "menus" not in self.loadeds:
            menus=__import__(self.label+".menus").menus

            for menu in settings.MENUS:

                if menu in menus.menus:
                    for item in menus.menus[menu]:
                        build(settings.MENUS[menu],item)
                    
            self.loadeds.append("menus")
    
                            
                    

    def add_menu(self,view,method):
        settings.MENUS["ADMIN_MENU"].append(ChatBotView.permissions["index"])

    def load_requests(self,**kwargs):
        import os
        if "requests" not in self.loadeds:      
            if os.path.exists(self.path+"/requests.py"):
                __import__(self.label+".requests").requests
                self.loadeds.append("requests")
            elif os.path.exists(self.path+"/requests"):
                __import__(self.label+".__init__.py")
                self.loadeds.append("requests")

    def load_actions(self,**kwargs):
        import os
        if "actions" not in self.loadeds:       
            if os.path.exists(self.path+"/actions.py"):
                __import__(self.label+".actions").actions
                self.loadeds.append("actions")
            elif os.path.exists(self.path+"/actions"):
                __import__(self.label+".__init__.py")
                self.loadeds.append("actions")
    def load_actions(self,**kwargs):
        import os
        if "filters" not in self.loadeds:       
            if os.path.exists(self.path+"/filters.py"):
                __import__(self.label+".filters").filters
                self.loadeds.append("filters")
            elif os.path.exists(self.path+"/filters"):
                __import__(self.label+".__init__.py")
                self.loadeds.append("filters")

    def load_urls(self,**kwargs):

        if "urls" not in self.loadeds:      
            if os.path.exists(self.path+"/urls.py"):
                from django.conf import settings
                
                __import__(self.label+".views").views
                __import__(self.label+".urls").urls
                
                self.loadeds.append("urls")
   
    def is_blocked(self,name):
        list_process=get_process()
        if not os.path.exists(self.name+"/.block"):
            with open(self.name+"/.block","w") as f:
                f.write("")

        with open(self.name+"/.block") as f:
            process=f.read().split("\n")
        
        for elem in process:
            result=search_process(list_process,task="/bin/sh -c "+name,
                pid=elem)    
            if result:
                return True
        else:
            return False


    def register_process(self,proc):        
        global process
        process.append(proc)
    
    def webpack(self):
        """
        Dada el nombre de la aplicacion se procede a crear el archivo de mezcla 
        para el webpack, esto es asi porque se espera que se compile cuando por 
        la url se accesa a un slug que pertenesca a dicha aplicacion
        """
        from django.utils.autoreload import file_changed,autoreload_started
        def killer(sender,**kwargs):
            self.observer.stop()
            print("THREADS:",self.threads)

        file_changed.connect(killer)
        autoreload_started.connect(watchdog_plugin)
        if sys.argv[1]=="runserver":
            if os.environ.get('RUN_MAIN'):
        
                self.observer = Observer()
             
                

                for (dirpath, dirnames, filenames) in os.walk("./"+self.name+"/static/"+self.name+"/py/"):
                    
                    if not ("node_modules" in dirpath or 
                        "__target__" in dirpath or 
                        "/dist" in dirpath ):

                        self.observer.schedule(MyEventHandler(self.name),
                        dirpath)
                    
                self.observer.start()

                def alive():
                    try:
                        while self.observer.is_alive():
                            self.observer.join(1)
                    except KeyboardInterrupt:
                        self.observer.stop()
                    self.observer.join()
                
        
                """      
                """  
                thread=threading.Thread(target=alive)
                self.threads.append(thread)
                thread.start()
                
    def sass(self):
        if sys.argv[1]=="runserver":
            import subprocess
            proc = subprocess.Popen(
                ["sass","--watch",f"{self.name}/scss:{self.name}/css"],
                stdout=subprocess.PIPE,
                cwd=self.name+'/static/'
            )
            self.register_process(proc)
            """
            thread=threading.Thread(target=sass_compile)
            self.threads.append(thread)
            thread.start()
            """
    def register_template(self,path,options,overwrite=False):
        """
        Este metodo esta pensado para los posts de paginas las cuales se les
        asigna un template, el template de dicho post puede que tenga alguna 
        configuracion especifica, esta configuracion se coloca en un json en 
        el content del post, sin embargo tambien se deberan registrar esa configuracion
        para el template de forma que esos campos puedan crearse para el proximo 
        post que quiera usar este template 
        """
        l=[]
        from asenzor.widgets import WidgetBox
        if path not in templates or overwrite:
            templates[path]=options
        elif path  in templates and not overwrite:
            raise Exception(f"El template '{path}'ya posee su configuración")


        if type(options)==dict:
            for option in options:
                for elem in options[option]:

                    if isinstance(elem,WidgetBox) and elem.name not in l:
                        pass
                    elif not isinstance(elem,WidgetBox) and elem["name"] not in l:
                        pass
                    else:
                        raise Exception(f"El campo '{elem['name']}' ya existe, este deber ser unico")
        
    def get_templates(self):
        return templates
    def get_template(self,path):
        return copy(templates[path])
    def compile_template_settings(self,path):
        from asenzor.widgets import WidgetBox
        page={}
        l=[]
        options=self.get_template(path)
        if type(options)==dict:
            for option in options:
                for elem in options[option]:

                    if type(elem)==WidgetBox:
                        page[elem.name]=elem.render()
                    else:
                        #widget=getattr(forms,elem["type"])()
                        page[elem["name"]]=elem["value"]

                    
  
    def compile_template_admin_settings(self,path,request,post=None):
        from asenzor.widgets import WidgetBox
        from django import forms
        from collections import OrderedDict
        import asenzor.widgets
        global widgets
        page=OrderedDict()
        l=[]
     
        options=self.get_template(path)
        if not options:
            return {}


        if type(options)==dict:

            for option in options:
                page[option]={}
                
                for elem in options[option]:
                    
                      
                    if isinstance(elem,WidgetBox) and elem.name not in l:
                        value=""
                      
                        if post:

                            if elem.name in post[option]:
                                elem.group=option
                                
                                for name in elem.fields:
                                    value=post[option][elem["name"]]["value"][name]
                                    if type(value)!=str:
                                        value=json.dumps(value)
                                    elem.value[name]=value
                                page[option][elem.name]=elem.render_settings(request)
                            
                        else:
                           
                            page[option][elem.name]=elem.render_settings(request)
                            
                    elif elem["type"] in dir(forms):
                      
                        widget=getattr(forms,elem["type"])(attrs=elem["options"] if "options" in elem else {})

                        
                        widget.attrs["name"]=option+"."+elem["name"]
                        value=""
                        if post:
                            if elem["name"] in post[option]:
                                value=post[option][elem["name"]]["value"]
                            if type(value)!=str:
                                value=json.dumps(value)
                        else:
                            if "value" in elem:
                                value=elem["value"]
                           
                                
                        widget.attrs["value"]=value
                        page[option][elem["name"]]=widget.render(option+"."+elem["name"],value)
                       

                    elif elem["type"] in dir(asenzor.widgets):
                       
                        widget=getattr(asenzor.widgets,elem["type"])()
                        widget.attrs.update(elem["options"] if "options" in elem else {})
                        widget.attrs["name"]=option+"."+elem["name"]
                        value=""
                      
                        if post:
                     
                            if elem["name"] in post[option]:
                                value=post[option][elem["name"]]["value"]
                            
                            if type(value)!=str:
                                value=json.dumps(value)
                        else:
                            if "value" in elem:
                                value=elem["value"]
                       
                        widget.attrs["value"]=value
                        
                        
                        page[option][elem["name"]]=widget.render(option+"."+elem["name"],value)

                    elif elem["type"] in widgets:
                        widget=getattr(widgets,elem["type"])()
                        widget.attrs.update(elem["options"] if "options" in elem else {})
                        widget.attrs["name"]=option+"."+elem["name"]
                        
                        value="" 
                        if post:
                            
                            if elem["name"] in post[option]:
                                value=post[option][elem["name"]]["value"]
                            if type(value)!=str:
                                value=json.dumps(value)
                        else:
                            if "value" in elem:
                                value=elem["value"]
                         
        
                        widget.attrs["value"]=value
                        page[option][elem["name"]]=widget.render(option+"."+elem["name"],value)
             

                        

        return page
    def serialize_template_admin_settings(self,path,request=None):
        from asenzor.widgets import WidgetBox
    
        options=self.get_template(path)
      
        page={}
        l=[]
       
        if type(options)==dict:
            for option in options:
                page[option]={}

                for elem in options[option]:
                   
                    if isinstance(elem,WidgetBox) and elem.name not in l:             
                        page[option][elem.name]=elem.to_json()
                    else:
                        page[option][elem["name"]]=elem
                        if "value" not in elem:
                            page[option][elem["name"]]["value"]=None

        return page
    def get_data_page(self,post=None):
        from asenzor.models import Post
        post=Post.objects.get(id=post)
        try:
            page=json.loads(post.content)
        except:
            page={}
        data={}

        for elem in page:
            data[elem]={}
            for elem2 in page[elem]:
                if "value" in page[elem][elem2]:
                    data[elem][elem2]=ValueAttr(page[elem][elem2]["value"],elem2,page[elem][elem2]["options"] if "options" in page[elem][elem2] else {})
         
                else:
                    data[elem][elem2]=""
        return data
    def get_serializable_page(self,post=None):
        from asenzor.models import Post
        post=Post.objects.get(id=post)
        if post.content:
            try:
                page=json.loads(post.content)
            except:
                page={}
        else:
            page={}
        data={}
        if page:
            for elem in page:
                data[elem]={}
                for elem2 in page[elem]:
                    if "value" in page[elem][elem2]:
                        data[elem][elem2]=page[elem][elem2]["value"]
             
                    else:
                        data[elem][elem2]=""
        return data


                  

  