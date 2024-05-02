from django.contrib import admin
from .models import *


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Recipes Details', {'fields': [
         'title', 'description', 'slug', 'cover', 'category']}),
        ('Preparation Details', {'fields': [
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
        ]}),
        ('Advanced', {'fields': ['preparation_step_is_html',
         'is_published', 'author'], 'classes': ['collapse']})
    ]

    list_display = [
        'id',
        'title',
        'created_at',
        'preparation_step_is_html',
        'is_published'
    ]

    list_display_links = [
        'title',
        'created_at'
    ]

    list_filter = [
        'is_published',
        'created_at',
        'category',
    ]
    search_fields = [
        'title',
        'description',
        'preparation_steps',
    ]

    list_per_page = 10

    list_editable = ['is_published']

    ordering = ['-id']

    prepopulated_fields = {
        'slug': ['title']
    }


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
