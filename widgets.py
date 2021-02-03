from django.forms import widgets
from django.template.loader import render_to_string
from copy import copy
hooks={}
templates={}#
import re
from django.utils.html import mark_safe

def camel_to_snake(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
def camel_to_snake2(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()

class MetaWidgetBox(type):
    def __new__(self,name,bases,attrs):

        fields={}      
        for elem in attrs:
            if elem not in ['__module__', '__qualname__', 'Meta', '__init__', 
                            'add', '__getitem__', 'render', 'render_settings',
                            "to_json","attrs"]:
                fields[elem]=attrs[elem]
                if not isinstance(attrs[elem],widgets.Widget):
                    raise  Exception(f"Solo estan permitidos parametros tipo {widgets.Widget}. '{elem}' no lo es")
      
        attrs["fields"]=fields

        attrs["__children__"]=[]
        return type(name,bases,attrs)
class WidgetBox:
    group=None
    named=False
    attrs={}
    class Meta:
        template=None
    def __init__(self,name,hook=None,value={}):
        fields={}      
        for elem in dir(self):
            if elem not in ['render', 'render_settings',"Meta","add","group","named",
                            "to_json","attrs"] and not (elem.startswith("__") and elem.endswith("__")):
                fields[elem]=getattr(self,elem)
                if not isinstance(getattr(self,elem),widgets.Widget):
                    raise  Exception(f"Solo estan permitidos parametros tipo {widgets.Widget}. '{elem}' no lo es")
        
        self.fields=fields
        for elem in self.fields:
            if "name" not in self.fields[elem].attrs:
                self.fields[elem].attrs["name"]=name+"_"+elem
            if ":name" not in self.fields[elem].attrs:
                self.fields[elem].attrs[":name"]="'"+name+"_"+elem+"'"
        self.fields[elem].attrs
        
        self.__children__=[]

      
        self.name=name
        self.value={}
        self.parent=None
        self.fullname=""

        if hook!=None:
            if hook in hooks:
                hooks[hook].append(self)
            else:
                hooks[hook]=[self]
    def add(self,widget):
        if widget not in self.__children__:
            widget.parent=self
            widget.fullname=self.name+"."+widget.name
            self.__children__.append(widget)
    def __getitem__(self,key):
        if key=="name":
            return self.name 
        elif key=="value":
            return self.value


    def render(self,request,data={}):
        d=data 
        d["request"]=d
        return render_to_string(self.Meta.template,d)
    def render_settings(self,request,data={}):
        from django.template import Template, Context

        template=f"<div name='{self.name}'>"
        for elem in self.fields:
            #toma los valores del content 
            value=None
            if elem in self.value:
                value=self.value[elem]
            
            self.fields[elem].attrs[":ref"]="'"+elem+"'"
            self.fields[elem].attrs["name"]=self.group+"."+self.name+"."+elem
            self.fields[elem].attrs[":name"]="'"+self.group+"."+self.name+"."+elem+"'"
            template+="<div>"+self.fields[elem].render(self.group+"."+elem,value)+"</div>"

        
        """
        for elem in self.__children__:
            template+=elem.render_settings()
        """
       
        template+="</div>"
 
        template = Template(template)
        context = Context(data)
        rendered: str = template.render(context)
     
        return rendered

    def to_json(self):
        value={}
        for elem in self.fields:
            value[elem]=self.fields[elem].attrs["value"] if "value" in self.fields[elem].attrs else None 

        d={"name":self.name,
           "type":self.__class__.__name__,
           "option":[],
           "value":value,
           }
        return d

class Widget(widgets.Widget):
    """docstring for Widget"""
    template_name=None
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        global templates      
        if "component" not in dir(self):
            self.component= camel_to_snake2(self.__class__.__name__)
        if "component_template" in dir(self):
            templates[self.component]=self.component_template
    def template_render(self,template,name,value):
        from django.template import Template, Context
        context = self.get_context(name, value, self.attrs)
        t=Template(template)
        c = Context(context)
        return mark_safe(t.render(c))
    def _render(self, template_name, context, renderer=None):
        pass





class ImageSelect(Widget):
    component_template="asenzor/widgets/ImageSelect.html"

    def render(self,name,value):
        return self.template_render("<image-select {% include 'asenzor/widgets/attrs.html'%}/>",name,value)

class Slider(Widget):
    component="slider-admin"
    component_template="asenzor/widgets/slider-admin.html"
    def render(self,name,value):
        
        return self.template_render("<slider-admin {% include 'asenzor/widgets/attrs.html'%}/>",name,value)
    

class Embeded(Widget):
    component="embeded-template"
    component_template="asenzor/widgets/embeded.html"
    def render(self,name,value):
        return self.template_render("<embeded {% include 'asenzor/widgets/attrs.html'%}/>",name,value)


class Video(Widget):
    def render(self,name,value):
        return self.template_render("<video-widget {% include 'asenzor/widgets/attrs.html'%}/>",name,value)

class SimpleMenu(Widget):
    component="simple-menu"
    component_template="asenzor/widgets/simple-menu.html"
    def render(self,name,value):
        return self.template_render("<simple-menu {% include 'asenzor/widgets/attrs.html'%}/>",name,value)

class Color(Widget):
    component="color-template"
    component_template="asenzor/widgets/color.html"
    def render(self,name,value):
        return self.template_render("<el-color-picker {% include 'asenzor/widgets/attrs.html'%} show-alpha></el-color-picker/>",name,value)


class TinyMCE(Widget):
    def render(self,name,value):
        import html,json
        from copy import copy
        if ":init" not in self.attrs:
            self.attrs[":init"]="""{
             height: 500,
             menubar: false,
             plugins: [
               "advlist autolink lists link image charmap print preview anchor",
               "searchreplace visualblocks code fullscreen",
               "insertdatetime media table paste code help wordcount",
               "textcolor"
             ],
             toolbar:
               "undo redo | formatselect | bold italic backcolor forecolor| \
               alignleft aligncenter alignright alignjustify | \
               bullist numlist outdent indent | removeformat |code insert| help"
           }"""
        print("#############", "value" in self.attrs)
        value=self.attrs["value"]
        if "value" in self.attrs:
            print("|||||||||||||||||||||||||||")
            self.attrs["initial-value"]=self.attrs["value"]
        self.attrs["value"]=value
        self.attrs["initial-value"]=self.attrs["value"][2:-2]
        print("@@@@@@@@",self.attrs["name"],self.attrs["initial-value"])
        return self.template_render("<button data-target='{{widget.name}}' >Insertar medio</button><div><editor {% include 'asenzor/widgets/attrs.html'%}  @onSelectionChange='function(value){update_content({\"{{widget.attrs.name}}\":value.target.body.innerHTML})}'/></div>",name,value)
