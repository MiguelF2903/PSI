from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)


# --- REQUISITO DEL TEST: test_challenge_part4_two ---
# Debemos crear un Inline para ver los libros DENTRO del autor
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0  # Requisito del test


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]  # Añadimos el inline aquí


admin.site.register(Author, AuthorAdmin)


# --- REQUISITO DEL TEST: test_new_added_book_visualizations ---
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # Requisito del test (eliminar filas vacías extra)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
