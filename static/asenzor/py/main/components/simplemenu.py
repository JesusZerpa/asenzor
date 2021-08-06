__pragma__("alias","s","$")
from .components.vuepy import VuePy


class SimpleMenu(VuePy):
    template="#simple-menu"
    methods=["add","remove","change","forceRerender"]

    def data(self):
        return {"menu":[],
                "name":self.vue["$attrs"]["name"],
                "c":0,
                "renderComponent": True}
    async def mounted(self):
        console.log("nnnnnnnn",self)
        menu=await self.vue["$root"].get_content(self.vue["$attrs"]["name"])
        if not menu:
            menu=[]
        c=0
        for elem in menu:
            if elem.id>c:
                c=elem.id+1
        self.vue.menu=menu
        self.vue.c=c
    async def forceRerender(self):
        #Remove my-component from the DOM
        self.vue.renderComponent = False;
        async def tick():
            self.vue.renderComponent = True;
        self.vue["$nextTick"](await tick);
      
    async def add(self):

        self.vue["menu"].append({"name":"","link":"#","id":self.vue["c"],"checked":False})
        self.vue["c"]+=1
        await self.vue.forceRerender()

    
    async def remove(self,name):
        l=[]
        for elem in self.vue["menu"]:
            if not elem.checked:
                l.append(elem)
        self.vue["menu"]=l

        await self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue["menu"]})

    async def change(self):
        await self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue["menu"]})

