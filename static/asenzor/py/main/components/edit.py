__pragma__("alias","s","$")
from .components.vuepy import VuePy
from .components.image_select import ImageSelect
from .components.tiny import TinyEditor
from .components.video import Video
from .components.simplemenu import SimpleMenu
from .components.embeded import Embeded
from .components.colorpicker import Color

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
    methods=["publish","save","update_from_widget",
             "update_content","get_content","get_by_type",
             "edit_guid_method","main_image_method",
             "open_modal"]
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
                "edit_guid":False,
                "author":None,
                "order":None,
                "password":None,
                "type":None,
                "template":None,
                "main_image":None,
                "toogle":self.toogle,
                "type":"post",
                "guid":None,
                "status":"public",
                "models":models}
    async def edit_guid_method(self):
        vue=self.vue
        vue.edit_guid=False
        console.log(vue.guid)
        form=__new__(FormData)()
        form.append("guid",vue.guid)
        form.append("id",POST_ID)
        req=await fetch("/json/posts/",{
            "body":form,
            "method":"PATCH"
            })
        data=await req.json()
        vue.guid=data["item"]["guid"]
    async def mounted(self):
        vue=self.vue
        vue.order=POST_ORDER
        if POST_ID:
            
            DATA=await self.get_data()
            console.log("qqqqq",DATA)
       
            content=DATA["content"] if DATA["content"] else ""
            if not content:
                content={}
            
            vue.content=content
            vue.guid=DATA["guid"]
            vue.status=DATA["status"]
            console.log("FFFFFFFFFFF",vue.status)
         
            if POST_MAIN_IMAGE:
                vue.main_image=POST_MAIN_IMAGE
            vue.title=DATA["title"] if DATA["title"] else ""

            color=(await vue.get_by_type("Color"))
            console.log("XXXXXXXX",color)
            for name,widget in color.items():
                    if "v-model" in dict(widget["options"]).keys(): 
                        console.log("*************")
                        if widget["options"]["v-model"].split(".")[0]=="models":
                            console.log("++++++++++")
                            vue.models[widget["options"]["v-model"].split(".")[1]]=widget["value"]
                        else:
                            console.log("MMMMMMM")
                            console.error("v-model solo se permite bajo el formato models.[name-model]")
      
            vue.template=TEMPLATE
            for elem in dict(vue["$refs"]).keys():

                if elem.startswith("toogle-"):
                    vue["$refs"][elem]
                    vue.toogle[elem]=True
         
        
            
            vue["type"]=DATA["type"]
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
        """
 

    async def update_from_widget(self,evt,value,name):
        """
        Este metodo de pruena esta diseñado para actualizar la informacion
        desde elementos de widgets normales de django, deberia usarse con @change
        """
        
        if await self.get_type(name)=="Color":
            """
            Esto es un parche que funciona al que el color 
            se cambie solo al color del comienzo al hacer click 
            fuera 
            """
            node=document.querySelector(f"[name='{name}'] .el-color-picker__color-inner")
            def callback(mutations):
                node.style.backgroundColor=value
                observer.disconnect();
            observer = __new__(MutationObserver)(callback);
            options = {
                "childList": True,
                "attributes": True,
            };
            observer.observe(node,options);
            

            node.style.backgroundColor=value
            self.vue.models[name.split(".")[1]]=value
    
        

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
        vue=self.vue
        form=__new__(FormData)()
        form.append("title",vue.title)
        form.append("type",POST_TYPE)
        form.append("menu_order",vue.order)
        if vue.status=="private":
            form.append("password",vue.password)
        form.append("status",vue.status)
        if POST_BUILDER=="custom":
            content=JSON.stringify(vue.content)
            form.append("content",content)
        else:
            form.append("content",vue.content)
        __pragma__("jsiter")
        req=await fetch("/json/posts/",{
            "body":form,
            "method":"POST"
            })
        __pragma__("nojsiter")
        if req.status==200:
            self.alert("Creado con exito")
        else:
            self.alert("A ocurrido un error","warning")
        data=await req.json()
        post=data["item"]
        vue.guid=data["item"]["guid"]
        form=__new__(FormData)()
        for elem in self.extra_data.keys():
            form.append(elem,self.extra_data[elem])
        form.append("post",post["id"])

        form.append("template",vue.template)
        form.append("main_image",vue.main_image)

        __pragma__("jsiter")
        req=await fetch("/json/postmeta/",{
            "body":form,
            "method": "POST"
            })
        __pragma__("nojsiter")

    async def save(self):
        vue=self.vue
        form=__new__(FormData)()
        form.append("title",vue.title)
        form.append("type",POST_TYPE)
        form.append("menu_order",vue.order)
        if vue.status=="private":
            form.append("password",vue.password)
        form.append("status",vue.status)
        DATA=await self.get_data()
        form.append("id",POST_ID)
        if POST_BUILDER=="custom":
            content=JSON.stringify(vue.content)
            form.append("content",content)
        else:
            form.append("content",vue.content)
        __pragma__("jsiter")
        req=await fetch("/json/posts/",{
            "body":form,
            "method":"PATCH",
            })
        __pragma__("nojsiter")
        
        if req.status==200:
            await self.alert("Actualizado con exito")
        else:
            await self.alert("A ocurrido un error","warning")
        data=await req.json()
        window.POST_ID=data["item"]["id"]
        post=data["item"]
        vue.guid=data["item"]["guid"]
       
        form=__new__(FormData)()

        for elem in self.extra_data.keys():
            form.append(elem,self.extra_data[elem])
        form.append("post",post["id"])
        form.append("template",vue.template)
        form.append("main_image",vue.main_image)

        __pragma__("jsiter")
        req=await fetch("/json/postmeta/",{
            "body":form,
            "method":"PATCH"
            })
        __pragma__("nojsiter")
    async def set_image_method(self,value):
        vue=self.vue
        console.log(value[0])
        vue.main_image=value[0].src

    async def main_image_method(self):
        lib=await window.media
        await lib.clear()

        await lib.vue["$on"]("accept",await self.set_image_method)
        modal=M.Modal.getInstance(document.querySelector("#media_modal"))
        modal.open()
    def insertContent(self,id,value):
        for elem in value:
            tinyMCE.js_get(id
                ).execCommand(
                'mceInsertContent', False, f"<img src='/media/{elem.src}'>");
            
        pass    
    async def open_modal(self,event):
        lib=await window.media
        type=await self.get_type(event.target.dataset.target)
      
        if type=="TinyMCE":
            id=event.target.nextSibling.children[0].id
            await lib.vue["$on"]("accept",lambda value:self.insertContent(id,value))
        await lib.clear()

        modal=M.Modal.getInstance(document.querySelector("#media_modal"))
        modal.open()
        pass


    

    async def alert(self,text,status=""):

        M.toast({"html":text,
                 "class":status})

    async def update_content(self,data):
        vue=self.vue
        for elem,value in dict(data).items():
            name=elem.split(".")
          
            if len(name)==2:

                vue.content[name[0]][name[1]]["value"]=value
            elif len(name)==3:
                vue.content[name[0]][name[1]]["value"][name[2]]=value
                
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
    async def get_type(self,name):  
        DATA=await self.get_data()
        if DATA["content"]:  
            name=name.split(".")
            if len(name)==2:
                return DATA["content"][name[0]][name[1]]["type"]
            elif len(name)==3:
                return DATA["content"][name[0]][name[1]]["value"][name[2]]["type"]
        else:
            return None
    async def get_by_type(self,type):
        components={}  
        DATA=await self.get_data()

        if typeof(DATA["content"])=="object":  

            for elem in dict(DATA["content"]).keys():
                
                for elem2 in dict(DATA["content"][elem]).keys():
                    if type==DATA["content"][elem][elem2]["type"]:
                        components[elem+"."+elem2]=DATA["content"][elem][elem2]
        return components
    async def get_data(self):

        if "POST_ID" in dir(window):
            if "DATA" not in dir(window):
                req=await fetch(f"/json/posts/{POST_ID}/")
                if (req.status==200):
                    data=await req.json()
                    item=data["item"]
                    window.DATA=item
                    if POST_BUILDER=="custom":
                        try:
                            
                            item["content"]=JSON.parse(item["content"])
                        except:

                            item["content"]={}
                else:
                    console.error("Error al obtener los datos:",req)
                return item
            else:
                return DATA
app=Edit()
