from copy import copy
class Div:

	def __init__(self,content="",attrs={"class":""},name=None,alias=None,closed=False):
		self.closed=closed
		self.attrs=copy(attrs)
		self.parentNode=None
		self.alias=alias
	
		if "class" not in self.attrs:
			self.attrs["class"]=""
		if type(content)==list:
			self.children=content

		else:
			self.children=[content]
		if name:
			self.__name__=name
		else:
			self.__name__=self.__class__.__name__.lower()

	def __setitem__(self,name,value):
		self.attrs[name]=value.replace('"','\"').replace("'","\'")
	def get(self,alias):

		for child in self.children:

			if type(child)!=str:
			
				if child.alias==alias: 
					return child
				else:
					child2=child.get(alias)
					if child2:
						return child2
		return None

	def __getitem__(self,name):
		return self.attrs[name]
	def add(self,component):
		self.children.append(component)
	def addClass(self,_class):
		if not self.hasClass(_class):
			self.attrs["class"]+=" "+_class
	def replaceClass(self,_class):
		if self.hasClass(_class):
			self.removeClass(_class)
		self.addClass(_class)
	def removeClass(self,_class):
		classes=[]
		for elem in self.attrs["class"].split():
			if elem!=_class:
				classes.append(elem)
		self.attrs["class"]=" ".join(classes)
		
	def hasClass(self,_class):
		return _class in self.attrs["class"].split()

	def __str__(self):
		content=""
		attrs=""
		classes=[]
		for elem in self.attrs["class"].split():
			if elem not in classes:
				classes.append(elem)
		self.attrs["class"]=" ".join(classes)
		for elem in self.attrs:
			attrs+=f'{elem}="{self.attrs[elem]}" '

		for child in self.children:
			content+=str(child)
		
		if self.closed:
			return "<"+self.__name__+" "+attrs+" />"
		else:
			return "<"+self.__name__+" "+attrs+" >"\
			+content+"</"+self.__name__+">"

class Button(Div):pass
class Image(Div):pass

class Section(Div):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.attrs["class"]="container"
		self.children.append(Div(
			Div(attrs={"class":"col md12"}),
			attrs={"class":"row"}))



class Card(Div):
	def __init__(self,title="",content="",action="",**kwargs):

		super().__init__(Div(
			[
			Div(title,attrs={"class":"card-title"}),
			Div(content),
			Div(action,attrs={"class":"card-action"})],
			attrs={"class":"card-content white-text"}),
		**kwargs)
		self.attrs["class"]="card blue-grey darken-1"
		
		self.__name__="div"

class CardImage(Div):
	def __init__(self,title="",action="",image="",**kwargs):
		super().__init__(Div(
			[
			Div([
				Image("",attrs={"src":image}),
				DIV(title,name="span",
					attrs={"class":"card-title"})
				],
				attrs={"class":"card-image"}
			),
			Div(action,attrs={"class":"card-action"})
			],
			attrs={"class":"card-content white-text"}),
		**kwargs)

		self.attrs["class"]="card blue-grey darken-1"
		
		self.__name__="div"

class CardButton(Div):
	pass

class CardHorizontal(Div):
	pass

class CardReveal(Div):
	pass

class CardTabs(Div):
	pass

class CardPanel(Div):
	pass

"""
<div class="row">
    <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">Card Title</span>
          <p>I am a very simple card. I am good at containing small bits of information.
          I am convenient because I require little markup to use effectively.</p>
        </div>
        <div class="card-action">
          <a href="#">This is a link</a>
          <a href="#">This is a link</a>
        </div>
      </div>
    </div>
  </div>
"""

class Link(Div):
	def __init__(self,href,**kwargs):
		kwargs["attrs"]={}
		kwargs["attrs"]["href"]=href
		kwargs["attrs"]["rel"]="stylesheet"
		
		super().__init__("",closed=True,**kwargs)
		self.children=[]

class Script(Div):
	def __init__(self,content="",**kwargs):
		print("ooooo",[content])
		super().__init__(content,**kwargs)



class Page(Div):
	def __init__(self,content=None,links=[],scripts=[],**kwargs):
		if content==None:
			card=Card()
			col=Div(card)
			col.addClass("col md12")
			row=Div(col)
			row.addClass("row")
			content=Div(row)
			content.addClass("container")
			card.children[0].children[0].alias="card.title"
			card.children[0].children[1].alias="card.content"
			card.children[0].children[2].alias="card.action"
		super().__init__(content,**kwargs)
		self.__name__="div"
		self.links=links
		self.scripts=scripts
	def head(self):
		head=""
		for elem in self.links:
			if type(elem)==str:
				head+=str(Link(elem))
			else:
				head+=elem
		
		for elem in self.scripts:
			if type(elem)==str:
				head+=str(Script("",attrs={"src":elem}))
				
			else:
				head+=str(elem)
		head+="""
		<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

		<meta name="viewport" content="width=device-width, initial-scale=1.0"/>

		"""
		return head
	def body(self):
		return super().__str__()

		
	def __str__(self):
		head=self.head()
		return f"<!DOCTYPE html><html><head>{head}</head><body>"+self.body()+"</body></html>"




class App(Page):
	def __init__(self,content=None,links=[],scripts=[],**kwargs):
		links=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]+links
		scripts=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"]+scripts
		super().__init__(content,links,scripts,**kwargs)
		content=self.children[0]
		content.attrs["id"]="app"
		content.attrs["template-inline"]=""
		self.add(Script(
		"""
		M.AutoInit();
		Devtools.mount("#app");
		"""))

