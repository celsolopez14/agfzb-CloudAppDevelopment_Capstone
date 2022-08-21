from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1 

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ('dealerId', 'car_type', 'car_year')

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ('car_name', 'car_description')
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
