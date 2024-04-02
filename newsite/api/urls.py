from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from api.view_authtoken import custom_obtain_auth_token
from api import views
# router = routers.DefaultRouter()
# router.register(r'',views.ArticleSerializerView)
# urlpatterns = [
#     path('list/',views.ArticleMixedAPIView.as_view()),
#     path('<int:pk>/',views.ArticleMixedAPIView.as_view()),
#     path('post/',views.ArticleMixedAPIView.as_view()),
#     path('post/<int:pk>/',views.ArticleMixedAPIView.as_view()),
#     path('delete/<int:pk>/',views.ArticleMixedAPIView.as_view()),
#     path('auth/',obtain_auth_token),
# ]
router = DefaultRouter()
router.register(r'articles',views.ArticleViewSet , basename='api_articles')
urlpatterns = router.urls + [path('auth/',custom_obtain_auth_token)] + [path('articles_search/',views.ArticleSearchAPI.as_view())] + [path('articles_mine/',views.ArticleMineAPI.as_view(),name = 'api_articles_mine')]
