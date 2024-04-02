from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from tags.models import AllTags
from django.db.models import Q

# Create your models here

class QuerySetC(models.QuerySet):
    def search(self,query,user = None):
        lookup = Q(title__icontains = query) | Q(author__username__icontains = query) | Q(article__icontains = query)
        qs = self.filter(lookup)
        if user is not None:
            qs = qs.filter(author = user)
        qs =qs.distinct()
        return qs
class ManagerC(models.Manager):
    def get_queryset(self):
        return QuerySetC(self.model , using=self._db)
    def search(self, query , user = None):
        return self.get_queryset().search(query,user=user)

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.TextField()
    objects = ManagerC()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("all_articles")
    def get_reverse_author(self):
        return self.author.get_username()[::-1]
    @property
    def get_reverse_title(self):
        return self.title[::-1]

class Tag(models.Model):
    article = models.ForeignKey(Article, related_name="tags", on_delete=models.CASCADE)
    tag = models.CharField(max_length=40)
    def __str__(self):
        return self.tag

class Comment(models.Model):
    The_Article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_commment = models.CharField(max_length=500)

    def __str__(self):
        return self.writer.get_username() + f" ({self.id})"

    def get_absolute_url(self):
        return reverse("all_articles")
