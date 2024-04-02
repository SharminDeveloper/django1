from rest_framework.authtoken.models import Token
from articles.models import Article
from tags.models import AllTags
def token_to_username(raw_token:str):
    token = raw_token[6:-1] + raw_token[-1]
    username = Token.objects.get(key = token).user.username 
    return username
class TagChanges:
    def __init__(self,pk,the_list):
        self.the_list = the_list
        self.all_tags = Article.objects.get(id = pk).tags
    def tag_exist_then_remove(self):
        for tag in self.the_list:
            if self.all_tags.filter(tag = tag).exists():
                self.all_tags.get(tag = tag).delete()
    def tag_exist_or_add(self):
        for tag in self.the_list:
            if not self.all_tags.filter(tag = tag).exists():
                self.all_tags.create(tag = tag)
                if not AllTags.objects.filter(tag = tag).exists():
                    AllTags.objects.create(tag = tag)
    def tag_set(self):
        self.all_tags.all().delete()
        for tag in self.the_list:
            self.all_tags.create(tag = tag)
            if not AllTags.objects.filter(tag = tag).exists():
                AllTags.objects.create(tag = tag)