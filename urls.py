from django.urls import path
from .views import *
from django.conf.urls.static import static
urlpatterns=[
path("",dashboard),
path("install/",install),
path("customize/",customize),
path("preview/",preview),
path("login/",login),
path("builder/",builder),
path("builder/<id>",builder),
]+static("wiki/", document_root="asenzor/doc/_build/html/")
CustomizeUser("user/",urlpatterns,"customize_user")
Posts("posts/",urlpatterns,"posts")
Forms("forms/",urlpatterns,"forms")
Pages("pages/",urlpatterns,"pages")
Media("media/",urlpatterns,"media")
Options("options/",urlpatterns,"options")
Plugins("plugins/",urlpatterns,"plugins")
Support("support/",urlpatterns,"support")
PageTemplate("page-template",urlpatterns,"page_template")