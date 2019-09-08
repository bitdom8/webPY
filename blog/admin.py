from django.contrib import admin
from .models import *



class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status" )
    # http://127.0.0.1:8000/admin/blog/post/  right bar there is filter APPEARS in admin page
    list_filter= ("status", "author")
    search_fields = ("author__username", "status", "content")

    list_editable = ("status",)

    data_hierarchy = ("created", )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(MyModel)
admin.site.register(Gallery)


# Register your models here.
