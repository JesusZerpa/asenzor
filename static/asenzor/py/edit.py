__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy
from .asenzor.py.image_select import ImageSelect
from .asenzor.py.tiny import TinyEditor
from .asenzor.py.video import Video
from .asenzor.py.simplemenu import SimpleMenu
from .asenzor.py.embeded import Embeded
from .asenzor.py.colorpicker import Color

#element=require("element-ui")

Editor=require("@tinymce/tinymce-vue")["default"]

window.VUE_COMPONENTS["asenzor"]['editor']=TinyEditor().__component__
window.VUE_COMPONENTS["asenzor"]["image-select"]=ImageSelect().__component__
window.VUE_COMPONENTS["asenzor"]["video-widget"]=Video().__component__
window.VUE_COMPONENTS["asenzor"]["simple-menu"]=SimpleMenu().__component__
window.VUE_COMPONENTS["asenzor"]["embeded"]=Embeded().__component__
window.VUE_COMPONENTS["asenzor"]["color"]=Color().__component__

Vue=require("vue")["default"]


class Edit(VuePy):
    """docstring for MyAoo"""   
    methods=["publish","save","update_from_widget","update_content","get_content","get_by_type"]
    components=window.VUE_COMPONENTS["asenzor"]
    content=""
    js_type=None
    template=None 
    main_image=None
    author=None
    order=None
    extra_data={}
    toogle={}
    title=None
    def created(self):
        window.edit=self.vue
    def data(self):
        #este metodo en vue nunca sera asyncrono
        models={}
        return {"content": "",
                "title": "",
                "status":None,
                "author":None,
                "order":None,
                "type":None,
                "template":None,
                "main_image":None,
                "toogle":self.toogle,
                "post_type":POST_TYPE,
                "type":"post",
                "models":models}
    async def mounted(self):
        vue=self.vue
        content=(await self.get_data())["post"]["content"] if (await self.get_data())["post"] else ""
        title=(await self.get_data())["post"]["title"] if (await self.get_data())["post"] else ""
        color=(await vue.get_by_type("Color"))
        for name,widget in color.items():
                if "v-model" in dict(widget["options"]).keys(): 
                    if widget["options"]["v-model"].split(".")[0]=="models":
                        vue.models[widget["options"]["v-model"].split(".")[1]]=widget["value"]
                    else:
                        console.error("v-model solo se permite bajo el formato models.[name-model]")
        self.vue.template=TEMPLATE
        for elem in dict(self.vue["$refs"]).keys():
            if elem.startswith("toogle-"):
                self.vue["$refs"][elem]
                self.vue.toogle[elem]=True
     
        """
        if self.vue.post_type=="custom":
            self.vue.content=
        """
        
        self.vue.order=POST_ORDER
        self.vue["type"]=(await self.get_data())["type"]
        """
        if self.vue["$refs"]["editor"]:
            console.log("dddddddd",self.vue["$refs"]["editor"]["$attrs"]["name"])
            self.vue.content=document.querySelector(
                "[data-name='"+self.vue["$refs"]["editor"]["$attrs"]["name"]+"']"
                ).value
        """
      
        def sticky():
          
            altura = s('.panel2').offset().top;
            altura = s('.navbar').offset().top;
            
            def switch():
            
                if ( s(window).scrollTop() > altura ):
                    s('.panel2').addClass('panel2-fixed');
                else:
                    s('.panel2').removeClass('panel2-fixed');
            s(window).on('scroll',switch)
        
    
        s(document).ready(sticky)
     
 

    def update_from_widget(self,evt,value,name):
        """
        Este metodo de pruena esta diseñado para actualizar la informacion
        desde elementos de widgets normales de django, deberia usarse con @change
        """
        if name:
            console.log({
                name:value
                })
            self.update_content({
                name:value
                })
        else:
            console.log({
                evt.target["name"]:evt.target.value
                })
            self.update_content({
                evt.target["name"]:evt.target.value
                })
       

    async def publish(self):
        form=__new__(FormData)()
        form.append("title",self.vue.title)
        form.append("type",self.vue["type"])
        form.append("menu_order",self.vue.order)
        form.append("status","publish")
        if window.DATA["post"]:
            form.append("id",await self.get_data()["id"])
        console.log("xxxxxx",self.vue.post_type)
        if self.vue.post_type=="custom":
            content=JSON.stringify(self.vue.content)
            form.append("content",content)
        else:
            form.append("content",self.vue.content)
        req=await fetch("/json/posts/",{
            "body":form,
            "method":"POST"
            })
        if req.status==200:
            self.alert("Creado con exito")
        else:
            self.alert("A ocurrido un error","warning")
        data=await req.json()
        post=data["item"]
       
        form=__new__(FormData)()
        for elem in self.extra_data.keys():
            form.append(elem,self.extra_data[elem])
        form.append("post",post["id"])
        form.append("template",self.vue.template)

        __pragma__("jsiter")
        req=await fetch("/json/postmeta/",{
            "body":form,
            "method":"PATCH" if await self.get_data()["id"]!=js_undefined else "POST"
            })
        __pragma__("nojsiter")

    async def save(self):
        alert("guardar")
        form=__new__(FormData)()
        form.append("title",self.vue.title)
        form.append("type",self.vue["type"])
        form.append("menu_order",self.vue.order)
        form.append("status","trash")
        DATA=await self.get_data()
        console.log("eeeeee",DATA)
        form.append("id",DATA["id"])
        console.log("xxxxxx",self.vue.post_type)
        if self.vue.post_type=="custom":
            content=JSON.stringify(self.vue.content)
            form.append("content",content)
        else:
            form.append("content",self.vue.content)
        
        


        req=await fetch("/json/posts/",{
            "body":form,
            "method":"PATCH" if await self.get_data()["id"]!=js_undefined else "POST",
            })
        console.log(req.status)
        if req.status==200:
            await self.alert("Actualizado con exito")
        else:
            await self.alert("A ocurrido un error","warning")
        data=await req.json()
        post=data["item"]
       
        form=__new__(FormData)()
        for elem in self.extra_data.keys():
            form.append(elem,self.extra_data[elem])
        form.append("post",post["id"])
        form.append("template",self.vue.template)

        __pragma__("jsiter")
        req=await fetch("/json/postmeta/",{
            "body":form,
            "method":"PATCH" if await self.get_data()["id"]!=js_undefined else "POST"
            })
        __pragma__("nojsiter")

    

    async def alert(self,text,status="success"):
        node=s("""<div id="alert" class="alert alert-dismissible fade show" style="position: fixed;top:20px;right: 20px" role="alert">
          {}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>""".format(text))
        node.addClass("alert-"+status)

        s(document.body).append(node)

    async def update_content(self,data):
        for elem,value in dict(data).items():
            name=elem.split(".")
            console.log([elem,value])
            if self.vue.content:
                if len(name)==2:

                    self.vue.content[name[0]][name[1]]["value"]=value
                elif len(name)==3:
                    self.vue.content[name[0]][name[1]]["value"][name[2]]=value
                    
    async def get_content(self,name):  
        DATA=await self.get_data()
        if DATA["content"]:  
            name=name.split(".")
            if len(name)==2:
                return DATA["content"][name[0]][name[1]]["value"]
            elif len(name)==3:
                return DATA["content"][name[0]][name[1]]["value"][name[2]]
        else:
            return None
    async def get_by_type(self,type):
        components={}  
        DATA=await self.get_data()
        if  DATA["content"]:  
            for elem in dict(DATA["content"]).keys():
                
                for elem2 in dict(DATA["content"][elem]).keys():
                    if type==DATA["content"][elem][elem2]["type"]:
                        components[elem+"."+elem2]=DATA["content"][elem][elem2]
        return components
    async def get_data(self):
        if "DATA" not in dir(window):
            req=await fetch(f"/json/posts/{POST_ID}/")
            data=await req.json()
            item=data["item"]
            window.DATA=item
            item["content"]=JSON.parse(item["content"])
            return item
        else:
            return DATA
app=Edit()
