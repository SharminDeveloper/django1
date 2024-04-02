from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListView, name="all_articles"),
    path("article/<int:pk>/", views.SpecificDetailView, name="article"),
    path("article/edit/<int:pk>/", views.EditUpdateView, name="edit_article"),
    path(
        "article/delete/<int:pk>/",
        views.SpecificDeleteView.as_view(),
        name="delete_article",
    ),
    path("article/create/", views.SpecificCreateView, name="create_article"),
    # path('article/<int:pk>/create_comment/',views.CommentCreateView.as_view(),name='create_comment'),
]
