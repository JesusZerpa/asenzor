from django import template
from django.http import HttpResponse,HttpResponseRedirect
register = template.Library()
import logging,coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


@register.filter
def list_item(lst, i):

    try:
        return lst[i]
    except:
        return None
@register.filter
def get_field(lst,model):
	return model._meta.get_field(lst)

@register.filter
def get_field_label(lst,model):
	
	if "verbose_name" in dir(model._meta.get_field(lst.lower())):
		return model._meta.get_field(lst.lower()).verbose_name
	else:
		pass
		#return model._meta.get_field(lst.lower())

@register.simple_tag
def get_field_value(lst,model,list1,field):
	print("wwwwwww",lst,model,list1,field)
	if model:
		field_object=model._meta.get_field(list1[lst])

		if "value_from_object" in dir(field_object):
			return field_object.value_from_object(field)
		else:
			pass
			#return field_object
	else:
		return field[list1[lst]]
@register.filter
def json(value):
	import json
	return json.dumps(value)
	
@register.filter
def join(lst, i):
	
	return i.join(lst)
@register.filter
def actions(actions_list, i):
	btns=""
	if actions_list[i]:

		for btn in actions_list[i]:
			logger.warning(btn)
			btns+="<a href='{}' class='{}' data-type='{}' >{}</a>".format(btn["url"],btn["class"] if "class" in btn else "",btn["type"] if "type" in btn else "get",btn["label"])
	return btns

@register.filter
def do_widget(field):
	from django import forms
	
	from main.forms import TemplateForm,SortableSelectMultiple,TemplateForm
	#from multiselectfield.forms.fields import MultiSelectFormField
	#from easy_select2.widgets import Select2TextInput
	print("####>>>>>>>",field)
	class Form(TemplateForm):
		"""docstring for Form"""
		
		def __init__(self,*args,**kwargs):
			
			super(Form,self).__init__(*args,**kwargs)
			
			if field.widget=="Select":
				self.fields[field.name]=forms.CharField(label=field.label,
														widget=forms.Select(choices=field.attributes["choices"]))
						
			elif field.widget=="SelectMultiple":	
				self.fields[field.name]=forms.CharField(label=field.label,
														
														widget=forms.SelectMultiple(choices=field.attributes["choices"],)
														)
			
			elif field.widget=="SortableSelectMultiple":
				#widget=MultiSelectFormField(choices=field.attributes["choices"])
				"""
				widget.is_hidden=False
				widget.attrs={}
				widget.id_for_label=field.label
				"""
				self.fields[field.name]=forms.CharField(label=field.label,
														widget=SortableSelectMultiple(
															choices=field.attributes["choices"],
															default=field.value),
														)

						
			
	form=Form()
	
	return form.as_p()
@register.filter 
def prueba(valor):
	return valor+"2"
@register.filter 
def json(valor):
	import json
	from django.utils.html import mark_safe
	return mark_safe(json.dumps(valor,indent=4, sort_keys=True))
@register.simple_tag 
def do_shortcode(valor):
	return valor
@register.simple_tag
def apply_filter(hook,result,**kwargs):

	from asenzor.lib.flow_control.filters import filters
	from django.utils.safestring import SafeString
	html=filters.apply_filters(hook,result,**kwargs)

	return SafeString(html)
@register.filter
def key(item,value):
	return item[value]

@register.filter
def show_type(item):
	return type(item)