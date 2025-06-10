from django.contrib import admin
from .models import Book, Category, Sale

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'stock')
    search_fields = ('title', 'authors', 'isbn')
    list_filter = ('category',)

    def stock_status(self, obj):
        return "Low" if obj.stock < 10 else "OK"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('book', 'date', 'qty')

# admin.site.register(Book, BookAdmin)
# admin.site.register(Category)