from django.contrib import admin
from .models import Entry, Tag, Author, Category

# Register your models here.
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'about', 'author', 'category', 'get_permalink',)
    # readonly_fields = ('get_permalink', )
    list_filter = ('title', 'date', 'author', 'category',)
    search_fields = ['title', 'date', 'author']
    order = ['date']
    fieldsets = (
        ('Entrada', {'fields': ('title', 'about', 'text', 'photo', 'active', 'top',)}),
        ('Autor', {'fields': ('author',)}),
        ('Categoria', {'fields': ('category', 'tags',)}),
    )

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
            'https://s3-us-west-1.amazonaws.com/static-dev-ilgiallorosso/js/ckeditor/ckeditor.js',
            'https://s3-us-west-1.amazonaws.com/static-dev-ilgiallorosso/js/admin/textareaentry.js',
        )

        css = {
            'ckeditor': ('https://s3-us-west-1.amazonaws.com/static-dev-ilgiallorosso/css/reset_ckeditor.css', )
        }

admin.site.register(Entry, EntryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'pic', 'get_permalink',)
    list_filter = ('name', 'short_description', 'pic',)
    search_fields = ['name']
    fieldsets = (
        ('General', {'fields': ('name', 'short_description', 'pic',)}),
    )
    order = ['name']
admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_filter = ('tag',)
    search_fields = ['tag']
    order = ['tag']
    fieldsets = (
        ('Tag', {'fields': ('tag',)}),
    )
admin.site.register(Tag, TagAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_about',)
    list_filter = ('user', 'short_about',)
    search_fields = ['user']
    fieldsets = (
        ('Usuario', {'fields': ('user', 'short_about', 'photo',)}),
    )
    order = ['user']
admin.site.register(Author, AuthorAdmin)
