from django.contrib import admin
from .models import UserGiallorosso

# Register your models here.
class UserGiallorossoAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'pic', 'social_media_user', 'active',)
    list_filter = ('user', 'birth_date', 'active',)
    search_fields = ['user', 'birth_date']
    fieldsets = (
        ('Usuario', {'fields': ('user', 'birth_date', 'social_media_user', 'active',)}),
    )
    ordering = ['user', 'active', 'social_media_user']
admin.site.register(UserGiallorosso, UserGiallorossoAdmin)