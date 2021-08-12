from django import forms
from django.contrib import admin
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.admin.widgets import ForeignKeyRawIdWidget,FilteredSelectMultiple,RelatedFieldWidgetWrapper
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper,EditSelectedWidgetWrapper,AddAnotherEditSelectedWidgetWrapper
from sortedm2m.forms import SortedCheckboxSelectMultiple
#from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple
#from searchableselect.widgets import SearchableSelect
#from dal import autocomplete

#pip install django-addanother
import os,sys
# Create your models here.
from .models import  Post
import json

from django import forms
from codemirror import CodeMirrorTextarea

codemirror_widget = CodeMirrorTextarea(
    mode="python",
    theme="cobalt",
    config={
        'fixedGutter': True
    },
)


class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url
        print("\nyyyyyyy\n")


    def render(self, name, value, *args, **kwargs):
        
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append('<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append('<img src="%sadmin/img/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))
from django.template import loader

class SortableSelectMultiple(forms.Widget):
	template_name="widgets/sortedmultiselect.html"
	def __init__(self,choices,default="",*args,**kwargs):
		super(SortableSelectMultiple,self).__init__(*args,**kwargs)
		self.choices=choices
		self.value=default
		
	def value_from_datadict(self, data, files, name):
		pass
	def render(self,name, value, attrs=None,*args, **kwargs):
		"""
		"""

		from main.libs.transcrypt import compiler2
		from uuid import uuid4
		from django.conf import settings		

		kwargs["widget_id"]=uuid4()
		kwargs["choices"]=self.choices
		kwargs["name"]=name
		kwargs["value"]=self.value
		kwargs["script"]=settings.BASE_URL+"static/"+compiler2("python/components/sortableselect/sortableselect.py")

	
		return mark_safe(render_to_string(self.template_name,kwargs))

		
class TemplateModelForm(forms.ModelForm):
	"""docstring for TemplateModelForm"""
	class Media:
		## media for the FilteredSelectMultiple widget
		css = {
		'all':('/static/admin/css/widgets.css',
			   "/static/sortedm2m/widget.css",
			   ),
		}
	class Meta:
		fields="__all__"
			
	@property
	def media(self):
		extra = '.min'
		
		js = [
            'core.js',
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
            "calendar.js",
            "admin/DateTimeShortcuts.js",
            #sortedm2m

            
            'admin/RelatedObjectLookups.js',
            "../../sortedm2m/widget.js",
            "../../sortedm2m/jquery-ui.js",
            'actions%s.js' % extra,
            'urlify.js',
            'prepopulate%s.js' % extra,
            'vendor/xregexp/xregexp.min.js',
            
		]
		return forms.Media(js=['admin/js/%s' % url for url in js])
	QUERY_SETS={}
	def __init__(self,*args,**kwargs):
		super(TemplateModelForm,self ).__init__(*args,**kwargs)
		from django.contrib.admin import widgets
		app=sys.modules[self.Meta.model.__module__].__file__.split("/")[-2]#esto es falso no todas pertenecen a este modelo
		if "model" not in dir(self._meta):
			raise Exception(f"El formulario '{self.__class__.___name__}' necesita un modelo")
		

		for elem in self.fields:
			print(self.fields[elem].widget.__class__.__name__,elem)
			if "RELATIONS" in dir(self._meta.model):
				if self.fields[elem].__class__.__name__=="SortedMultipleChoiceField":
					app,model=self._meta.model.RELATIONS[elem].split(".")
					
					choices=self.fields[elem].widget.choices
					from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
					if "RELATIONS_CONTROLS" in dir(self._meta.model) and elem in self._meta.model.RELATIONS_CONTROLS:
						
						widget=SortedCheckboxSelectMultiple()
						if "horizontal_filter" in self._meta.model.RELATIONS_CONTROLS[elem]:
							widget=SortedFilteredSelectMultiple()
							#widget=widgets.FilteredSelectMultiple(widget)

						if "add" in self._meta.model.RELATIONS_CONTROLS[elem] and "edit" in self._meta.model.RELATIONS_CONTROLS[elem]:
							self.fields[elem].widget=AddAnotherEditSelectedWidgetWrapper(
								widget,
								"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
								edit_related_url="/admin/{}/{}/__fk__/change/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
								)
						elif "add" in self._meta.model.RELATIONS_CONTROLS[elem]:
							self.fields[elem].widget=AddAnotherWidgetWrapper(
								widget,
								"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
								)
						if "edit" in self._meta.model.RELATIONS_CONTROLS[elem]:
							self.fields[elem].widget=EditSelectedWidgetWrapper(
								widget,
								edit_related_url="/admin/{}/{}/__fk__/change/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
								)
					else:
						"""
						self.fields[elem].widget=AddAnotherWidgetWrapper(
							SortedCheckboxSelectMultiple(),
							"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
							)
						"""
					self.fields[elem].widget.choices=choices

				elif self.fields[elem].__class__.__name__=="ModelMultipleChoiceField":
					app,model=self._meta.model.RELATIONS[elem].split(".")
					widget=self.fields[elem].widget
					
					choices=self.fields[elem].widget.choices
					if elem in self.QUERY_SETS:
						choices=self.QUERY_SETS[elem]

					#widget=forms.SelectMultiple()
					

					if "RELATIONS_CONTROLS" in dir(self._meta.model) and elem in self._meta.model.RELATIONS_CONTROLS:

						

						
						if "add" in self._meta.model.RELATIONS_CONTROLS[elem] and "edit" in self._meta.model.RELATIONS_CONTROLS[elem]:
							
							self.fields[elem].widget=AddAnotherEditSelectedWidgetWrapper(
							widget,
							"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
							edit_related_url="/admin/{}/{}/__fk__/change/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
							)
						elif "add" in self._meta.model.RELATIONS_CONTROLS[elem]:
							self.fields[elem].widget=AddAnotherWidgetWrapper(
								widget,
								"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
								)
						if "edit" in self._meta.model.RELATIONS_CONTROLS[elem]:
							self.fields[elem].widget=EditSelectedWidgetWrapper(
								widget,
								edit_related_url="/admin/{}/{}/__fk__/change/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
								)
						
					else:
						
						self.fields[elem].widget=AddAnotherWidgetWrapper(
							forms.SelectMultiple(),
							"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
							)
						
					self.fields[elem].widget.choices=choices
					
				elif self.fields[elem].__class__.__name__=="ModelChoiceField":
					app,model=self._meta.model.RELATIONS[elem].split(".")
					choices=self.fields[elem].widget.choices
					if elem in self.QUERY_SETS:
						choices=self.QUERY_SETS[elem]
					self.fields[elem].widget=AddAnotherWidgetWrapper(
						forms.Select(),
						"/admin/{}/{}/add/?_to_field=id&_popup=1".format(app,model.lower()),#reverse_lazy('resources_new'),
						)
					self.fields[elem].widget.choices=choices


			if self.fields[elem].widget.__class__.__name__=="DateInput":

				self.fields[elem]=forms.CharField(label=self.fields[elem].label,widget=forms.TextInput(attrs={"class":"datepicker"}))#widgets.AdminDateWidget()
			if self.fields[elem].widget.__class__.__name__=="TimeInput":

				self.fields[elem]=forms.CharField(label=self.fields[elem].label,widget=forms.TextInput(attrs={"class":"timepicker"}))#widgets.AdminDateWidget()

			if self.fields[elem].widget.__class__.__name__=="DateTimeInput":

				self.fields[elem]=forms.CharField(label=self.fields[elem].label,widget=forms.TextInput(attrs={"class":"datetimepicker"}))#widgets.AdminDateWidget()


				"""
				
				
                """
			if "READ_ONLY" in dir(self._meta.model) and elem in self._meta.model.READ_ONLY:
				self.fields[elem].widget.attrs["readonly"]="readonly"
'''
from material_widgets.forms import MaterialForm
class MaterialForm(MaterialForm):
	"""
	"""
	miprueba=forms.MultipleChoiceField(
		label="Escoje 1 o mas",
		help_text="ctrl + click to unselect",
		#widget=MaterialSelect
		choices=(
			("select Multiple 1",(
				("multiple_choice_1","Multiple choice 1"),
				("multiple_choice_2","Multiple choice 2"),
				("multiple_choice_3","Multiple choice 3"),
				)
				),
			("select Multiple 2",(
				("multiple_choice_4","Multiple choice 4"),
				("multiple_choice_5","Multiple choice 5"),
				("multiple_choice_6","Multiple choice 6"),
				),
			)

			)
		)
'''

class TemplateForm(forms.Form):
	"""docstring for TemplateModelForm"""
	class Media:
		## media for the FilteredSelectMultiple widget
		css = {
		'all':('/static/admin/css/widgets.css',
			   "/static/sortedm2m/widget.css",
			   ),
		}
	class Meta:
		fields="__all__"
	def __init__(self,*args,**kwargs):
		super(TemplateForm,self).__init__(args,kwargs)
		
			
	@property
	def media(self):
		extra = '.min'
		
		js = [
            'core.js',
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
            "calendar.js",
            "admin/DateTimeShortcuts.js",
            #sortedm2m

            
            'admin/RelatedObjectLookups.js',
            "../../sortedm2m/widget.js",
            "../../sortedm2m/jquery-ui.js",
            'actions%s.js' % extra,
            'urlify.js',
            'prepopulate%s.js' % extra,
            'vendor/xregexp/xregexp.min.js',
            
		]
		return forms.Media(js=['admin/js/%s' % url for url in js])

class PageTemplateForm(forms.Form):
	"""docstring for PageTemplateForm"""

	content=forms.CharField(label="Data",widget=codemirror_widget)
	field=forms.CharField(label="Widget",widget=codemirror_widget )
	action=forms.ChoiceField(label="Acción",
		choices=[("add","Añadir"),
				 ("remove","Eliminar")])
	class Meta:
		model=Post
	def __init__(self, *args,**kwargs):
		self.instance=None
		error=False
		if "instance" in kwargs:
			self.instance=kwargs["instance"]
			if len(args)>2:
				self.post=args[1]
				try:
					self.save()
				except:
					error=True
				widget=self.post.get("field")
			self.request=args[0]


			del kwargs["instance"]
		super().__init__(**kwargs)
		if self.instance:
			if self.instance.content:
				try:
					self.fields["content"].initial=json.dumps(json.loads(self.instance.content),indent=2)
				except Exception as e:
					self.fields["content"].initial={}
		
			if error:
				self.fields["field"].initial=widget

			pass
	def save(self):
		
		if self.instance:
			widget=self.post.get("field")
			if widget:
				if self.post.get("action")=="add":
					
					data=json.loads(self.instance.content) 
					data2=json.loads(widget)
					for elem in data2:
						data[elem].update(data2[elem])
					self.instance.content=json.dumps(data)
					self.instance.save()

				elif self.post.get("action")=="remove":
					
					data=json.loads(self.instance.content)
					name=widget.split(".")

					if len(name)==2:
						for elem in data[name[0]]:
							if name[1]==elem:
								del data[name[0]][elem]
								break
						self.instance.content=json.dumps(data)
					elif len(name)==1:
						del data[name[0]]
						self.instance.content=json.dumps(data)
			else:
				data=json.loads(self.post.get("content"))
				self.instance.content=json.dumps(data)

			self.instance.save()
		




		
		


class AttributeWidget(forms.Widget):
	"""docstring for Atribute"""
	template_name="widgets/attributeWidget.html"

class inputselectautocompleteWidget(forms.Widget):
	"""docstring for Atribute"""
	template_name="widgets/inputselectautocomplete.html"
		
class DynamicForm(forms.Form):
	def __init__(self,fields,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for elem in fields:
			if elem["type"] in ["TextInput","URLInput","NumberInput","EmailInput",
								"PasswordInput","HiddenInput","DateInput","DateTimeInput",
								"TimeInput","Textarea","CheckboxInput","Select","NullBooleanSelect",
								"SelectMultiple","RadioSelect","CheckboxSelectMultiple","FileInput",
								"ClearableFileInput","MultipleHiddenInput","SplitDateTimeWidget",
								"SplitHiddenDateTimeWidget","SelectDateWidget"]:
				self.fields[elem["name"]]=forms.CharField(elem["name"])
				if "options" not in elem:
					elem["options"]={}
				self.fields[elem["name"]].widget=getattr(forms,elem["type"])(**elem["options"])


class InstallForm(forms.Form):
	main_site=forms.CharField(label="Nombre del sitio",
		help_text="Nombre que tendra el sitio web")
	site_description=forms.CharField(label="Descripcion",
		help_text="Descripcion del sitio")


	class Meta:
		widgets={
		"main_site":forms.TextInput(),
		"site_description":forms.Textarea(),
		}

	def __init__(self,*args,**kwargs):
		super(InstallForm,self).__init__(*args,**kwargs)
		remove=[]
		print(dir(self))
		for elem in self.Meta.widgets:
			self.fields[elem].widget=self.Meta.widgets[elem]

		for field in self.fields:
			if field in remove:
				del self.fields[field]


