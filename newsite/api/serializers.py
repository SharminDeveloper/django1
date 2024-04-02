# from rest_framework import serializers
# from articles.models import Article

# class ArticleModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['title','author','article']
from django.contrib.auth import get_user_model
from rest_framework import serializers 
from articles.models import Article
from articles.models import Tag
class ArticleSubSetSerializer(serializers.Serializer):
    username = serializers.CharField(read_only = True)
    email = serializers.EmailField(read_only = True)
    id = serializers.IntegerField(read_only = True)
class UserToArticleSerializer(serializers.Serializer):
    title = serializers.CharField(read_only = True)
    link = serializers.HyperlinkedIdentityField(view_name='api_articles-detail',lookup_field = 'pk' ,read_only = True)
class TagSerializer(serializers.StringRelatedField):
    class Meta:
        model = Tag
        fields = ['tag']
class ArticleSerializer(serializers.ModelSerializer):
    author_identity = ArticleSubSetSerializer(source = 'author' , read_only = True)
    same_author_articles = UserToArticleSerializer(source = 'author.article_set.all',many = True , read_only = True)
    author_reversed = serializers.SerializerMethodField(read_only = True)
    title_reversed = serializers.SerializerMethodField(read_only = True)
    tags = TagSerializer(many=True, read_only=True )
    tag = serializers.ListField(child = serializers.CharField(max_length=40) , write_only = True ,default = [])
    tag_method = serializers.CharField(default = None , write_only = True)
    url = serializers.HyperlinkedIdentityField(view_name='api_articles-detail',lookup_field = 'pk')
    class Meta:
        model = Article
        fields = ['pk','url','author_identity','title', 'author', 'article', 'author_reversed','title_reversed','same_author_articles','tags','tag','tag_method']
    def create(self, validated_data):
        validated_data.pop('tag')
        validated_data.pop('tag_method')
        return super().create(validated_data)
    def get_author_reversed(self,obj):
        return obj.get_reverse_author()
    def get_title_reversed(self,obj):
        return obj.get_reverse_title
