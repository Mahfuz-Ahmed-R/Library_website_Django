from django.contrib import admin
from .models import Deposit, Book, Category, Borrow, RatingModel

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Deposit)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(RatingModel)