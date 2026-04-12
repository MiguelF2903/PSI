from django.contrib import admin
from .models import Song, SongUser


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'language',
                    'category', 'number_times_played',
                    'created_at')
    list_filter = ('language', 'category')
    search_fields = ('title', 'artist')


@admin.register(SongUser)
class SongUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'played_at',
                    'correct_guesses', 'wrong_guesses')
    list_filter = ('user', 'song')
