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
    post_type=None
    title=None
    def created(self):
        window.edit=self.vue
    def data(self):
        models={}
        for name,widget in self.get_by_type("Color").items():
                if "v-model" in dict(widget["options"]).keys():
                    models[widget["options"]["v-model"].split(".")[1]]=widget["value"]

        return {"content":window.DATA["post"]["content"] if window.DATA["post"] else "",
                "title":window.DATA["post"]["title"] if window.DATA["post"] else "",
                "status":None,
                "author":None,
                "order":None,
                "type":None,
                "template":None,
                "main_image":None,
                "toogle":self.toogle,
                "post_type":None,
                "type":"post",
                "models":models}
    def mounted(self):
        self.vue["post_type"]=self.vue["$el"]["attributes"]["post_type"]["value"]
        if window.DATA["post"]["content"]:
            console.log("wwwww",self.vue.get_by_type("Color"))
            for name,widget in self.vue.get_by_type("Color").items():
                if "v-model" in dict(widget["options"]).keys():
                    self.vue.models[widget["options"]["v-model"]]=widget["value"]
                    console.log("hhhh",self.vue.models[widget["options"]["v-model"]],widget["value"])
        self.vue.template=self.vue["$refs"]["template"].attributes["value"]["value"]

        for elem in dict(self.vue["$refs"]).keys():
            if elem.startswith("toogle-"):
                self.vue["$refs"][elem]
                self.vue.toogle[elem]=True
     
        """
        if self.vue.post_type=="custom":
            self.vue.content=
        """
        
        self.vue.order=self.vue["$refs"]["order"].attributes["value"]["value"]
        self.vue["type"]=self.vue["$refs"]["type"].attributes["data-value"]["value"]
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
        console.log("iiii")
 

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
            form.append("id",window.DATA["post"]["id"])
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
            "method":"PATCH" if window.DATA["post"]["id"]!=js_undefined else "POST"
            })
        __pragma__("nojsiter")

    async def save(self):
        form=__new__(FormData)()
        form.append("title",self.vue.title)
        form.append("type",self.vue["type"])
        form.append("menu_order",self.vue.order)
        form.append("status","trash")
        if window.DATA["post"]:
            form.append("id",window.DATA["post"]["id"])
        console.log("xxxxxx",self.vue.post_type)
        if self.vue.post_type=="custom":
            content=JSON.stringify(self.vue.content)
            form.append("content",content)
        else:
            form.append("content",self.vue.content)
        
        


        req=await fetch("/json/posts/",{
            "body":form,
            "method":"PATCH" if window.DATA["post"]["id"]!=js_undefined else "POST",
            })
        console.log(req.status)
        if req.status==200:
            self.alert("Actualizado con exito")
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
            "method":"PATCH" if window.DATA["post"]["id"]!=js_undefined else "POST"
            })
        __pragma__("nojsiter")

    

    def alert(self,text,status="success"):
        node=s("""<div id="alert" class="alert alert-dismissible fade show" style="position: fixed;top:20px;right: 20px" role="alert">
          {}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>""".format(text))
        node.addClass("alert-"+status)

        s(document.body).append(node)

    def update_content(self,data):
     
        for elem,value in dict(data).items():
            name=elem.split(".")
         
            if len(name)==2:
                self.vue.content[name[0]][name[1]]["value"]=value
            elif len(name)==3:
                self.vue.content[name[0]][name[1]]["value"][name[2]]=value
                
    def get_content(self,name):  
        if DATA["post"] and DATA["post"]["content"]:  
            name=name.split(".")
            if len(name)==2:
                return DATA["post"]["content"][name[0]][name[1]]["value"]
            elif len(name)==3:
                return DATA["post"]["content"][name[0]][name[1]]["value"][name[2]]
        else:
            return None
    def get_by_type(self,type):
        components={}  
        if DATA["post"] and DATA["post"]["content"]:  
            for elem in dict(DATA["post"]["content"]).keys():
                
                for elem2 in dict(DATA["post"]["content"][elem]).keys():
                    if type==DATA["post"]["content"][elem][elem2]["type"]:
                        components[elem+"."+elem2]=DATA["post"]["content"][elem][elem2]
                   
        return components
app=Edit()
