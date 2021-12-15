from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model= CarModel

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name')
    list_filter = ['name']
    search_fields = ['name', 'description']


class CarModelAdmin(admin.ModelAdmin):
    list_filter = ['model_year']

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
