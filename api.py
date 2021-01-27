from .lib.ResourceView import ResourceViewRest,serialize
from .models import Post,PostMeta,Option,User
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,multipartparser
import json,os
class Media(ResourceViewRest):
    """docstring for Pages"""
    model=Post
    filter={"type":"attachment"}
    def middleware(self,view,request,data):
        if view=="search":
            for elem in data["items"]:

                author=serialize(User.objects.get(id=elem["author"]),["email","id","username"])
                elem["author"]=author                
                url,ext=os.path.splitext(elem["guid"])
                elem["filesizeHumanReadable"]="97 KB"
                elem["filesizeInBytes"]=0
                
                if elem["mime_type"].lower() in ["image/jpeg","image/jpg","image/png","image/gif","image/bmp"]:

                    elem["sizes"]={ 
                    "full":{
                        "height": 600,
                        "orientation": "landscape",
                        "url":  url+"_600-600"+ext,
                        "width": 600},
                    "medium":{
                        "height": 300,
                        "orientation": "landscape",
                        "url":url+"_300-300"+ext,
                        "width": 300
                        },
                    "thumbail":{
                        "height": 150,
                        "orientation": "landscape",
                        "url": url+"_150-150"+ext,
                        "width": 150
                    }
                    }
            data["items"].reverse()

        if view=="post":
            url,ext=os.path.splitext(data["item"]["guid"])
            data["item"]["filesizeHumanReadable"]="97 KB"
            data["item"]["filesizeInBytes"]=0

            if data["mime_type"].lower() in ["image/jpeg","image/jpg","image/png","image/gif","image/bmp"]:
                
                    data["item"]["sizes"]={ 
                    "full":{
                        "height": 600,
                        "orientation": "landscape",
                        "url":  url+"_600-600"+ext,
                        "width": 600},
                    "medium":{
                        "height": 300,
                        "orientation": "landscape",
                        "url":url+"_300-300"+ext,
                        "width": 300
                        },
                    "thumbail":{
                        "height": 150,
                        "orientation": "landscape",
                        "url": url+"_150-150"+ext,
                        "width": 150
                    }
                    }
                    

class Plugin(ResourceViewRest):
    pass
    upload_path="asenzor/plugins/"
    def post(self,request):
        super().post(request)
        import requests
        if request.POST.get("action")=="download":
            name=request.POST.get("plugin").split()[-1]
            req=requests.get(request.POST.get("plugin"))
            with open("asenzor/plugins/"+name,"wb") as f:
                f.write(req.content)
            ruta_zip = "asenzor/plugins/"+name
            ruta_extraccion = "asenzor/plugins/"
            password = None
            archivo_zip = zipfile.ZipFile(ruta_zip, "r")
            try:
                print(archivo_zip.namelist())
                archivo_zip.extractall(pwd=password, path=ruta_extraccion)
            except:
                pass
            archivo_zip.close()
            asenzor.load_plugins()
        elif request.POST.get("action")=="upload":
            name=request.POST.get("plugin").split()[-1]
            req=requests.get(request.POST.get("plugin"))
            ruta_zip = "asenzor/plugins/"+name
            ruta_extraccion = "asenzor/plugins/"
            password = None
            archivo_zip = zipfile.ZipFile(ruta_zip, "r")
            try:
                print(archivo_zip.namelist())
                archivo_zip.extractall(pwd=password, path=ruta_extraccion)
            except:
                pass
            archivo_zip.close()
            name,ext=os.path.splitext(name)
            asenzor.load_plugins()
        item={}
        for elem in asenzor.get_plugins():
            if elem.__name__==name:
                item["name"]=elem.__name__
                item["description"]=elem.__doc__
                item["version"]=elem.__version__

        return JsonResponse({"headers":[],"item":item})


class Posts(ResourceViewRest):
    """docstring for Pages"""
    model=Post
    def middleware(self,view,request,data):
        if view=="post":
            if "name" not in data:
                name=data["title"].replace(" ","-")
                newname=name
                c=2
                while True:
                    
                    try:
                        self.model.objects.get(name=newname)
                        newname=name+f"-{c}"
                        c+=1
                    except:

                        break
                data["name"]=newname


            if "author" not in data:
                data["author"]=request.user.id


class Support(ResourceViewRest):
    """docstring for Pages"""
    model=Post
    subroutes=[
    ("update-parner","update_parner"),
    ("get-parner","get_parner"),
        ]
    def get_parner(self,request):
        user=self.token_auth(request)
        if user:
            return JsonResponse({
                "headers":[],
                "item":{
                "username":user.username,
                "description":UserMeta.get(user,"description")
                }
                })

    def update_parner(self,request):
        if request.method=="PATCH":
            token=request.PATCH.get("parner_token")
            token=Option.get("parner_token")
            req=requests.get("https://zerpatechnology.com.ve/asenzor/json/support/get-parner",)
            data=req.json()
            return JsonResponse(data)

class PostMeta(ResourceViewRest):
    """docstring for Pages"""
    model=PostMeta
    def put(self,request,id=None):
        post=int(request.POST.get("post"))
        post=Post.objects.get(id=post)
        d={}
        items=[]
        for key,value in request.POST.items():
            if key!="post":
                items=self.model.update(post,key,value)
        return JsonResponse({"_meta":[{"post":post}],"items":items})
    def patch(self,request,id=None):

        post=int(request.PATCH.get("post"))
        post=Post.objects.get(id=post)
        d={}
        items=[]
        for key,value in request.PATCH.items():
            if key!="post":
                
                items=self.model.update(post,key,value)
        return JsonResponse({"_meta":[{"post":post.id}],"items":items})

class Options(ResourceViewRest):
    """docstring for Pages"""
    model=Option


class CryptoPayment(ResourceViewRest):
    """docstring for Pages"""
    
    def index(self,request):
        import urlparse
        from lbcapi import api

        hmac_key = UserMeta.get("localbitcoins_hmmac_key") #Your HMAC key here
        hmac_secret = UserMeta.get("localbitcoins_hmmac_secret") #Your HMAC secret here
        if hmac_key:
            conn = api.hmac(hmac_key, hmac_secret)
            ads_json = conn.call('GET', '/api/ads/').json()
            parsed = urlparse.urlparse(ads_json['pagination']['next'])
            params = urlparse.parse_qs(parsed.query)
            ads_json_II = conn.call('GET', '/api/ads/', params=params).json()
            {"address":"",
             "amount":0,
             }
            #ads_json_II = conn.call('POST', '/api/wallet-send/', params=params).json()
            #ads_json_II = conn.call('POST', '/api/logout/', params=params).json()
            #ads_json_II = conn.call('POST', "/api/wallet-send-pin/", params=params).json()
            #ads_json_II = conn.call('GET', "/api/myself/", params=params).json()
            #ads_json_II = conn.call('GET',"/api/notifications/", params=params).json()
            #ads_json_II = conn.call('GET',"/api/wallet/").json()
            #ads_json_II = conn.call('GET',"/api/wallet-balance/").json()
    def wallet(self,request):
        pass
    def myself(self,request):
        pass
    def notifications(self,request):
        pass
    def wallet_send(self,request):
        pass
    def wallet_balance(self,request):
        pass
        

        
        
            