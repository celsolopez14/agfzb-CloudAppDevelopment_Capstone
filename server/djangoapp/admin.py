from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    fields = ['dealerId','car_type','car_year']
    extra = 1 

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['dealerId','car_type','car_year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('car_name',)
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModelAdmin)
