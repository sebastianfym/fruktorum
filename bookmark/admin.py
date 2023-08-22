from django.contrib import admin

from bookmark.models import Bookmark, Collection


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'description', 'image_preview', 'url')


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Collection)
