from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, New, Contact

admin.site.register(Contact)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'body', 'category', 'publish_time', 'status', 'show_image',
    list_filter = 'title', 'publish_time', 'status',
    prepopulated_fields = {'slug': ('title', )}

    def show_image(self, obj: New):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    show_image.short_description = "Image"
