# from rest_framework import viewsets
# from .serializers import ArticleModelSerializer
# from articles.models import Article
# class ArticleSerializerView(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleModelSerializer
from typing import Any
from django.http import JsonResponse , HttpResponse,HttpResponseNotFound , QueryDict , HttpRequest , HttpResponseForbidden
import json
from articles.models import Article
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from api.serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import mixins , generics , viewsets , authentication
from api.authentication import CustomTokenAuthentication
from api.permissions import UserIsEqualToAuthor
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .functions import token_to_username , TagChanges
# def api(request):
#     try:
#         body = json.loads(request.body)
#     except: 
#         body = {}
#     response = {}
#     response ['headers'] = dict(request.headers)
#     response ['body'] = body
#     response ['params'] = dict(request.GET)
#     model_first_object = model_to_dict(Article.objects.all()[0])
#     response['data_base'] = model_first_object
#     return JsonResponse(response)



class ArticleMixedAPIView(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        try:
            if int(request.POST.get('author')) != int(request.user.id):
                return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()
        try:
            action = request.POST.get('action')
        except:
            return HttpResponseNotFound()
        if action == 'create':
            return self.create(request,*args,**kwargs) 
        elif action == 'update':
            if int(request.user.id) != int(self.queryset.get(id = kwargs.get(self.lookup_field)).author.id):
                return HttpResponseForbidden()
            return self.update(request,*args,**kwargs) 
        else :
            return HttpResponseNotFound()
    def delete(self,request,*args,**kwargs):
        try:
            if int(request.user.id) != int(self.queryset.get(id = kwargs.get(self.lookup_field)).author.id):
                return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()
        return self.destroy(request,*args,**kwargs)
    def perform_create(self, serializer): 
        serializer.save(author = self.request.user )
    def perform_update(self, serializer):
        serializer.save(author = self.request.user )
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    
    
    
    
@api_view(['GET'])
def api(request):
    model_object = Article.objects.all()[0]
    data = ArticleSerializer(model_object).data
    return Response(data)





class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication,CustomTokenAuthentication]
    permission_classes = [UserIsEqualToAuthor]
    model = Article
    pk = None
    token_user = None
    def dispatch(self, request, *args, **kwargs):   
        self.pk = kwargs.get(self.lookup_field)
        try:
            value = self.request.headers.get('Authentication')
            if value is None :
                value = self.request.headers.get('Authorization')
            self.token_user = token_to_username(value)
        except:
            pass
        return super().dispatch(request, *args, **kwargs)
    def perform_create(self, serializer):
        instance = serializer.save(author = get_user_model().objects.get(username = self.token_user))
        pk = instance.id
        the_list = serializer.validated_data['tag']
        TagChanges(pk,the_list).tag_set()
    def perform_update(self, serializer):
        serializer.save(author = get_user_model().objects.get(username = self.token_user))
        the_list = serializer.validated_data['tag']
        tag_method = serializer.validated_data['tag_method']
        if tag_method is not None:
            if tag_method == 'add':
                TagChanges(self.pk,the_list).tag_exist_or_add()
            elif tag_method == 'remove':
                TagChanges(self.pk,the_list).tag_exist_then_remove()
            elif tag_method == 'set':
                TagChanges(self.pk,the_list).tag_set()
            else:
                pass
class ArticleMineAPI(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def get_queryset(self,*args, **kwargs):
        qr = super().get_queryset(*args, **kwargs)
        value = self.request.headers.get('Authentication')
        if value is None :
            value = self.request.headers.get('Authorization')
        username = token_to_username(value)          
        user_instance = get_user_model().objects.get(username = username)
        filtered_qr = qr.filter(author = user_instance)
        return filtered_qr
class ArticleSearchAPI(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        username = self.request.GET.get('username')
        mine = self.request.GET.get('mine')
        results = Article.objects.all()
        if q is not None:
            if mine == 'true':
                try:
                    value = self.request.headers.get('Authentication')
                    if value is None :
                        value = self.request.headers.get('Authorization')
                    username = token_to_username(value) 
                    user = get_user_model().objects.get(username = username)    
                    results = qs.search(q,user = user)
                except:
                    results = qs.search(q)
            if get_user_model().objects.filter(username=username).exists():
                user = get_user_model().objects.get(username = username)
                results = qs.search(q,user = user)
            else:
                return qs.search(q)
        return results