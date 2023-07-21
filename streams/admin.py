from django.contrib import admin

from streams.models import Stream, Content, ContentCategory, ContentCategoryAssociation

# Register your models here.
admin.site.register(Stream)
admin.site.register(Content)
admin.site.register(ContentCategory)
admin.site.register(ContentCategoryAssociation)
