from django.contrib import admin
from .models import *


#OUTRO MÉTODO
class RecipeAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)

#MÉTODO MAIS FÁCIL
class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Category, CategoryAdmin)

# Register your models here.
