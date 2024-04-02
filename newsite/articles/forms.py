from django import forms
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["user_commment"]


class UpdateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "article"]


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    article = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 50}), required=True
    )
    tag = forms.CharField(max_length=40, required=False)
