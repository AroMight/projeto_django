from django.contrib import admin
from .models import *


#OUTRO MÉTODO
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Recipes Details', {'fields':['title', 'description','slug','cover','category']}),
        ('Preparation Details', {'fields':[
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            ]}),
        ('Advanced', {'fields':['preparation_step_is_html','is_published','author'],'classes':['collapse']})
        ]
    list_display = [
        'title',
        'updated_at',
        'created_at',
        'preparation_step_is_html',
        'is_published'
        ]
    list_filter=[
        'is_published',
        'created_at',
        'updated_at',
        'author'
        ]
    search_fields = [
        'title',
        ]

#MÉTODO MAIS FÁCIL
class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
