from django.contrib import admin
from .models import Article, Comment , Tag


# Register your models here.
class CommentInlines(admin.StackedInline):
    model = Comment
    extra = 0
class TagInlines(admin.StackedInline):
    model = Tag
    extra = 0 

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [TagInlines,CommentInlines]
    list_display = ["title", "author",'id']
    search_fields = ("title", "author", "body")
