__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy


class SimpleMenu(VuePy):
    template="#simple-menu"
    methods=["add","remove","change","forceRerender"]

    def data(self):

        menu=self.vue["$root"].get_content(self.vue["$attrs"]["name"])
        if not menu:
            menu=[]
        c=0
        for elem in menu:
            if elem.id>c:
                c=elem.id+1
        return {"menu":menu,
                "name":self.vue["$attrs"]["name"],
                "c":c,
                "renderComponent": True}
    def forceRerender(self):
        #Remove my-component from the DOM
        self.vue.renderComponent = False;
        def tick():
            self.vue.renderComponent = True;
        self.vue["$nextTick"](tick);
      
    def add(self):

        self.vue["menu"].append({"name":"","link":"#","id":self.vue["c"],"checked":False})
        self.vue["c"]+=1
        self.vue.forceRerender()

    
    def remove(self,name):
        l=[]
        for elem in self.vue["menu"]:
            if not elem.checked:
                l.append(elem)
        self.vue["menu"]=l

        self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue["menu"]})

    def change(self):
        console.log("&&&&&&&&&",self.vue["$root"])
        self.vue["$root"].update_content({self.vue["$attrs"]["name"]:self.vue["menu"]})

