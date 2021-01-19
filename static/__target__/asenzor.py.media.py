__pragma__("alias","s","$")
from .asenzor.py.vuepy import VuePy 
import re

class Media(VuePy):
    """docstring for Media"""
    methods=["select","drag","drop","upload","accept","edit","remove"]
    images=[]
    single=False
    mediatabs=0
    active=None

    def data(self):
        return {"images":[],
                "dragAndDropCapable": False, 
                "files": [],
                "uploadPercentage": 0,
                "selected":[],#los que estan en azul
                "desmark":[],#los que estan en gris
                "mediatabs":self.mediatabs,
                "active":None,
                "search":""
                 }


    def determineDragAndDropCapable(self):
        """
        Determines if the drag and drop functionality is in the
        window
        Create a test element to see if certain events
        are present that let us do drag and drop.
        """
        div = document.createElement('div');

        """
        Check to see if the draggable event is in the element
        or the ondragstart and ondrop events are in the element. If
        they are, then we have what we need for dragging and dropping files.

        We also check to see if the window has FormData and FileReader objects
        present so we can do our AJAX uploading
        """

        return ( ( 'draggable' in dir(div) )
            or ( 'ondragstart' in dir(div) and 'ondrop' in dir(div) ) )\
            and 'FormData' in window\
            and 'FileReader' in window;
    def mounted(self):
        """
        Determine if drag and drop functionality is capable in the browser
        """
        self.vue.dragAndDropCapable = self.determineDragAndDropCapable();
        """
        If drag and drop capable, then we continue to bind events to our elements.
        """
        if( self.vue.dragAndDropCapable ):
            """
            Listen to all of the drag events and bind an event listener to each
            for the fileform.
            """
            
            def for_events(evt):
                def add_event(e):
                    e.preventDefault();
                    e.stopPropagation();
                add_event.bind(self.vue)
                """
                For each event add an event listener that prevents the default action
                (opening the file in the browser) and stop the propagation of the event (so
                no other elements open the file in the browser)
                """
                self.vue["$refs"].fileform.addEventListener(evt,add_event,False)
            for_events.bind(self.vue)
            ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(for_events);
        """
        Add an event listener for drop to the form
        """
        def capture_files(e):
            """
            Capture the files from the drop event and add them to our local files
            array.
            """
            i = 0
            console.log("@@@@@",e.dataTransfer.files.length)
            while i < e.dataTransfer.files.length:
                self.vue.files.push( e.dataTransfer.files[i] );
                i+=1
            self.submitFiles()
            #self.getImagePreviews()
        capture_files.bind(this)
        self.vue["$refs"].fileform.addEventListener('drop', capture_files);
        __pragma__ ('jsiter') 
        fetch('/json/media/',
            {
            "method":"GET",
            })\
        .then(lambda res:res.json())\
        .then(self.drawImages)\
        .catch(lambda e:self.vue["$root"].alert(e,"danger") );
        __pragma__ ('nojsiter')
    def drawImages(self,data):
        
        files=[]

        for elem in data["items"]:
            
            files.append({
                "src":elem["guid"],
                "id":elem["id"],
                "alternative":"",
                "title":elem["title"] if elem["title"] else "",
                "name":elem["name"],
                "author":elem["author"]["username"],
                "description":elem["content"],
                "sizes":elem["sizes"]})
        self.vue.images=files 




    def getImagePreviews(self): 
        """ 
        Obtiene la vista previa de la imagen del archivo. 
        Itere todos los archivos y genere una vista previa de la imagen para cada uno. 
        """
        i=0

    
    def removeFile (self,clave):
        """
        Elimina un archivo seleccionado que el usuario ha subido 
        """
        self.vue.files.splice (clave, 1); 
    
    def submitFiles(self):
        """
        Submits the files to the server
        Initialize the form data
        """
        formData =__new__(FormData)();
        """
        Iteate over any file sent over appending the files
        to the form data.
        """
        i=0
        console.log(self.vue.files)
        while i < self.vue.files.length:
            file = self.vue.files[i];
            formData.append('files[' + i + ']', file);
            i+=1
        """
        Make the request to the POST /file-drag-drop URL
        """

        __pragma__ ('jsiter') 
        fetch('/json/media/',
            {
            "method":"POST",
            "body":formData,
            })\
        .then(lambda res:res.json())\
        .then(self.uploaded)\
        .catch(lambda e:console.log('FAILURE!!',e));
        __pragma__ ('nojsiter')
        self.vue.files=[]
        

    def onUploadProgress(self,progressEvent): 
        self.uploadPercentage = parseInt (Math.round ((progressEvent.loaded * 100) / progressEvent.total));
        self.uploadPercentage.bind(self.vue)
        

  
    def uploaded(self,data):
        item=data["item"]
        src=item["guid"]
        del item["guid"]
        item["src"]=src
        self.vue.images.push(item)


        if s(self.vue["$refs"]["tab1"]).hasClass("active"):
            s(self.vue["$refs"]["tab1"]).removeClass("active show")
        s(self.vue["$refs"]["tab2"]).addClass("active show")

    def upload(self):
        pass
    def drag(self):
        pass
    def drop(self):
        pass
    def clear(self):
        """
        Resetea los valores de la seleccion y desmarcados
        """
        self.vue.selected=[]
        self.vue.desmark=[]
        for elem in dict(self.vue["$refs"]).keys():
            if elem.startswith("slide_"):
                self.vue["$refs"][elem][0].style.border="inherit"
    def remove(self):
        pass

        __pragma__ ('jsiter') 
        fetch('/json/media/',
            {
            "method":"DELETE",
            "body":formData,
            })\
        .then(lambda res:res.json())\
        .then(self.deleted)\
        .catch(lambda e:console.log('FAILURE!!',e));
        __pragma__ ('nojsiter')
    def edit(self):
        __pragma__ ('jsiter') 
        fetch('/json/media/',
            {
            "method":"PUT",
            "body":formData,
            })\
        .then(lambda res:res.json())\
        .then(self.edited)\
        .catch(lambda e:console.log('FAILURE!!',e));
        __pragma__ ('nojsiter')
    def deleted(self,data):
        l=[]
        for elem in self.vue.images:
            if elem.id!=data["item"]:
                l.append(elem)
        self.vue.images=l
    def edited(self,data):
        pass

    def select(self,name):

        

        if not self.single:
            if self.vue.selected.includes(name):
                self.vue["$refs"][name][0].style.border="solid 2px gray"

                i=self.vue.selected.indexOf(name)
                self.vue.selected.splice(i,1)
                if not self.vue.desmark.includes(name):
                    self.vue.desmark.push(name)

            elif self.vue.desmark.includes(name):
                self.vue["$refs"][name][0].style.border="inherit"
                i=self.vue.desmark.indexOf(name)
                self.vue.desmark.splice(i,1)

            else:
                self.vue["$refs"][name][0].style.border="solid 2px blue"
                self.vue.selected.push(name)
                self.vue.active=self.activate(self.getdata(self.vue["$refs"][name][0].id))
        elif self.single:
            if len(list(self.vue.selected))==0:
                self.vue.selected.push(name)
                self.vue["$refs"][name][0].style.border="solid 2px blue"
                self.vue.active=self.activate(self.getdata(self.vue["$refs"][name][0].id))
            else:
                if self.vue.selected.includes(name):
                    i=self.vue.selected.indexOf(name)
                    self.vue.selected.splice(i,1)
                    self.vue["$refs"][name][0].style.border="inherit"
                else:
                    self.vue.selected[0]=name
                    for elem in dict(self.vue["$refs"]).keys():
                        if elem!=name:
                            self.vue["$refs"][name][0].style.border="inherit"

                    self.vue["$refs"][name][0].style.border="solid 2px blue"
                    self.vue.active=self.activate(self.getdata(self.vue["$refs"][name][0].id))
    def getdata(self,id):
        for img in self.vue.images:
            if img.id==int(id):
                return img
    def activate(self,data):
        return data


    def accept(self):
        selected=[]
        for elem in self.vue.selected:
            for img in self.vue.images:
                if img.id==int(self.vue["$refs"][elem][0].id):
                    selected.push(img)
        self.vue["$emit"]("accept",selected)
        s("#media_modal").modal("hide")
        self.off()




