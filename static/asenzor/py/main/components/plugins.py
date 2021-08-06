__pragma__("alias","s","$")
from .components.vuepy import VuePy 
class Plugins(VuePy):
    """docstring for Toolbar"""
    methods=["search","install"]
    plugins=[]
    showUpload=False

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
            
            while i < e.dataTransfer.files.length:
                self.vue.files.push( e.dataTransfer.files[i] );
                i+=1
            self.getImagePreviews()
            self.submitFiles()
        capture_files.bind(this)
        self.vue["$refs"].fileform.addEventListener('drop', capture_files);
        __pragma__ ('jsiter') 
        fetch('/json/media/',
            {
            "method":"GET",
            })\
        .then(lambda res:res.json())\
        .then(self.drawImages)\
        .catch(lambda e:console.log('FAILURE!!',e));
        __pragma__ ('nojsiter')
    def drawImages(self,data): 
        files=[]
        for elem in data["items"]:
            files.append({"src":elem["guid"]})
        self.vue.images=files 
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
        formData.append("type","upload")
        __pragma__ ('jsiter') 
        fetch('/json/plugins/',
            {
            "method":"POST",
            "body":formData,
            })\
        .then(lambda res:res.json())\
        .then(self.uploaded)\
        .catch(lambda e:console.log('FAILURE!!',e));
        __pragma__ ('nojsiter')
    def onUploadProgress(self,progressEvent): 
        self.uploadPercentage = parseInt (Math.round ((progressEvent.loaded * 100) / progressEvent.total));
        self.uploadPercentage.bind(self.vue)

    def data(self):
        console.log(window.DATA["plugins"])
        return {"plugins":window.DATA["plugins"],
                "dragAndDropCapable": False, 
                "files": [],
                "uploadPercentage": 0,
                "showUpload":False}
    def search(self):
        pass
    def install(self,id):
        form=__new__(FormData())
        form.append("id",id)
        form.append("type","remote")
        fetch("json/plugins/",
            {
            "method":"POST",
            "body":form
            })



