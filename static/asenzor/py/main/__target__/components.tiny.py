from .components.vuepy import VuePy 

Editor=require("@tinymce/tinymce-vue")["default"]

class TinyEditor(VuePy):
    """
    """
    extends=Editor
    methods=["setContent"]
    def data(self):

        return {"name":self.vue["$attrs"]["name"]}

    async def mounted(self):
        
        """
        def setInit():
            if self.vue["editor"]:

                self.vue["editor"].startContent="hola mundo"
                self.vue["editor"].setContent("Hola mundo")
        
            else:
                setTimeout(setInit,1000)
        setTimeout(setInit,1000)
        """

