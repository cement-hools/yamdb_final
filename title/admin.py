from django.contrib import admin

from title.models import Comment, Review, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text',)


admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentsAdmin)
