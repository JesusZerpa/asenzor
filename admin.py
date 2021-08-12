from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Option)
admin.site.register(Post)
admin.site.register(PostMeta)
admin.site.register(UserMeta)

admin.site.register(TermTaxonomy)
admin.site.register(Term)
admin.site.register(Comment)
admin.site.register(CommentMeta)
admin.site.register(Link)
admin.site.register(Site)
