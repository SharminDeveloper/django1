from django.test import TestCase
from .models import Article
from django.contrib.auth import get_user_model
# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(username = 'admin' , password = 'admin')
        self.article = Article.objects.create(title = 'test' , author = self.admin , article = 'njancjeanjkc')
    def test_first(self):
        login_url = '/login/'
        login = self.client.login(username='admin',password='admin')
        self.assertTrue(login)
        self.client.post('/articles/article/create/',{'title':'newtest','article':'njancjeanjk','tags':'[]','status':'done'})
        instance1 = Article.objects.all()[0].article
        instance2 = Article.objects.all()[1].article
        self.assertEqual(instance1,instance2)