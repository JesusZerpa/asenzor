Vue=require("vue")["default"]
__pragma__("js","{}","""
function clone(obj) {
    var copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}
""")
draggable=require('vuedraggable')

Vue.component("draggable",draggable)
class VuePy:
	"""docstring for VuePy"""
	methods=[]
	computed=[]
	watch=[]
	delimiters=['[[', ']]']
	__deployed__=False
	__link__=False
	async def __init__(self,*args,**kwargs):
		data={"methods":{},
			  "watch":{},
			  "compute":{}}
		

		for elem in dir(self):
			if elem not in ['__bases__', '__class__', '__init__', 
							'__metaclass__', '__module__', '__name__', 
							'__new__',"methods","computed",
							"watch","mount","deploy","__deployed__","__link__","data"]:
			
				if typeof(getattr(self,elem))=="function":
					getattr(self,elem).__name__=elem

				if elem in self.methods:
					def wrapper(self,elem):
						async def fn(*args):
							that=this
							self.vue=that
							d=await self[elem](*args)
							self.vue=that
							return d
						return fn 

					data["methods"][elem]=wrapper(self,elem)
				
			
				elif elem in self.computed:
					def wrapper(self,elem):
						async def fn(*args):
						
							that=this
							self.vue=that
							d=await self[elem](*args)
							self.vue=that
							return d
						return fn 

					data["computed"][elem]=wrapper(self,elem)
				elif elem in self.watch:
					def wrapper(self,elem):
						async def fn(*args):
						
							that=this
							self.vue=that
							d=await self[elem](*args)
							self.vue=that
							return d
						return fn 

					data["watch"][elem]=wrapper(self,elem)


				else:
					if typeof(getattr(self,elem))=="function":
						def wrapper(self,elem):
							async def fn(*args):
								that=this
								self.vue=that
								result=await self[elem](that,*args)
								self.vue=that
								return result

							return fn 
						data[elem]=wrapper(self,elem)
					else:
						if not self.__link__:
							data[elem]=clone(getattr(self,elem))

						else:
							data[elem]=getattr(self,elem)


		if "data" in dir(self):
			def wrapper(self,elem):
				def fn(*args):
					that=this

					self.vue=that
					return clone(self["data"](*args))
				return fn 
			if not self.__link__:
				data["data"]=wrapper(self,"data")
			
			else:
				data["data"]=getattr(self,"data")
		
		self.__component__=data
	def beforeCreate(self,vue):
		self.vue=vue
	def off(self,fn):
		if fn:
			for event in dict(self.vue._events).keys():
				for k,elem in enumerate(self.vue._events[event]):
					if elem==fn:
						self.vue._events[event][k].splice(k,1)
		else:
			self.vue._events=[]

	
	async def deploy(self):
		if not self.__deployed__:
			self.vue=__new__(Vue(self.__component__))
			self.__deployed__=True
		return self

	async def mount(self,el):
		await self.deploy()
		self.vue["$mount"](el)
		return self
	def updated(self):
		pass