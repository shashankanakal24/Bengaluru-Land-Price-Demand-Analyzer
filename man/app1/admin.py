from django.contrib import admin
from .models import Location, Prediction

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display in the list view
    search_fields = ('name',)  # Fields to search in the admin interface

admin.site.register(Location, LocationAdmin)

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('location', 'bhk', 'bath', 'sqft', 'prediction', 'created_at')
    list_filter = ('location', 'bhk', 'bath')
    search_fields = ('location',)
    readonly_fields = ('prediction', 'created_at')


admin.site.register(Prediction, PredictionAdmin)


