from errors.views import Error404, Error301
from django.http import HttpResponseRedirect, QueryDict, HttpResponseForbidden
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView, CreateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Article, Comment, Tag
from .forms import CommentForm, UpdateArticle, ArticleForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from tags.models import AllTags
import ast

# Create your views here.
# class ArticleListView(LoginRequiredMixin, ListView):
#     model = Article
#     template_name = "articles/articles.html"
#     context_object_name = "articles"


def ArticleListView(request):
    try:
        resault = request.GET.get("search")
        if resault == "":
            return HttpResponseRedirect("/" + "articles/")
        selected_articles = Article.objects.filter(
            Q(title__icontains=resault)
            | Q(author__username__icontains=resault)
            | Q(tags__tag__icontains=resault)
        ).distinct()
    except:
        selected_articles = Article.objects.all()
        resault = ""
    resault_found = selected_articles.count()
    return render(
        request,
        "articles/articles.html",
        {
            "articles": selected_articles,
            "resault_found": resault_found,
            "resault": resault,
        },
    )


# def ArticleListView(request):
#     try:
#         resault = request.GET.get("search")
#         search_vector = (
#             SearchVector("title", weight="B")
#             + SearchVector("author", weight="A")
#             + SearchVector("article", weight="D")
#         )
#         search_query = SearchQuery(resault)
#         search_rank = SearchRank(search_vector, search_query)
#         selected_articles = (
#             Article.objects.annotate(rank=search_rank)
#             .filter(rank__gte=0.4)
#             .order_by("-rank")
#         )
#     except:
#         selected_articles = Article.objects.all()
#     resault_found = selected_articles.count()
#     return render(
#         request,
#         "articles/articles.html",
#         {"articles": selected_articles, "resault_found": resault_found},
#     )


# class SpecificDetailView(LoginRequiredMixin,FormMixin,DetailView):
#     model = Article
#     template_name = 'articles/article.html'
#     context_object_name = 'article'
#     form_class = CommentForm
#     def post(self,*args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             Error404.as_view()(self.request)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm(initial={'writer':self.request.user,'The_Article':self.object})
#         return context
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#     def get_success_url(self):
#         return reverse('article',kwargs={'pk':self.object.id})
def SpecificDetailView(request, pk):
    try:
        article = Article.objects.get(id=pk)
        tags_len = len(article.tags.all())
        user_is_writer = []
        user_is_not_writer = []
        for comment in article.comments.all():
            if comment.writer == request.user:
                user_is_writer.append(comment)
            else:
                user_is_not_writer.append(comment)
    except:
        return Error404.as_view()(request)
    try:
        comment_status = request.GET.get("comment_status")
        current_comment = article.comments.get(id=request.GET.get("comment_pk"))
    except:
        comment_status = "None"
    if comment_status == "edit":
        if request.user == current_comment.writer:
            form = CommentForm(instance=current_comment)
        else:
            return Error301.as_view()(request)
    elif comment_status == "delete":
        if request.user == current_comment.writer:
            form = current_comment
        else:
            return Error301.as_view()(request)
    else:
        form = CommentForm()
    if request.method == "POST":
        if comment_status == "edit":
            form = CommentForm(request.POST, instance=current_comment)
        elif comment_status == "delete":
            current_comment.delete()
            return HttpResponseRedirect("/" + "articles/article/" + str(article.id))
        else:
            form = CommentForm(request.POST)
        if form.is_valid():
            if comment_status == "edit":
                form.save()
            else:
                obj = form.save(commit=False)
                obj.writer = request.user
                obj.The_Article = article
                obj.save()
            return HttpResponseRedirect("/" + "articles/article/" + str(article.id))
        else:
            return Error301.as_view()(request)
    return render(
        request,
        "articles/article.html",
        {
            "article": article,
            "form": form,
            "comment_status": comment_status,
            "user_is_not_writer": user_is_not_writer,
            "user_is_writer": user_is_writer,
            "tags_len": tags_len,
        },
    )


# class EditUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
#     model = Article
#     template_name = 'articles/edit_article.html'
#     fields = [
#         'title',
#         'article'
#     ]
#     def test_func(self):
#         return self.get_object().author == self.request.user


# def EditUpdateView(request, pk):
#     try:
#         article = Article.objects.get(id=pk)
#     except:
#         return Error404.as_view()(request)
#     form = UpdateArticle(instance=article)
#     if request.method == "POST":
#         form = UpdateArticle(request.POST, instance=article)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/" + "articles/" + "article/" + str(pk) + "/")
#         else:
#             return Error301.as_view()(request)
#     return render(
#         request, "articles/edit_article.html", {"article": article, "form": form}
#     )


class SpecificDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/delete_article.html"
    success_url = reverse_lazy("all_articles")

    def test_func(self):
        return self.get_object().author == self.request.user


# class SpecificCreateView(LoginRequiredMixin, CreateView):
#     model = Article
#     template_name = "articles/create_article.html"
#     fields = ["title", "article", "tags"]


#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
@login_required
def EditUpdateView(request, pk):
    try:
        get_article = Article.objects.get(id=pk)
    except:
        return Error404.as_view()(request)
    if request.user != get_article.author:
        return Error301.as_view()(request)
    if request.method == "POST":
        if request.POST.get("status") == "done":
            form = ArticleForm(request.POST)
            if form.is_valid():
                get_article.title = form.cleaned_data["title"]
                get_article.article = form.cleaned_data["article"]
                get_article.save()
                list_tags = request.POST.get("tags")
                list_tags = list_tags.strip()
                list_tags = ast.literal_eval(list_tags)
                for the_tag in list_tags:
                    if get_article.tags.filter(tag=the_tag).exists() == False:
                        Tag.objects.create(article=get_article, tag=the_tag)
                    if AllTags.objects.filter(tag=the_tag).exists() == False:
                        AllTags.objects.create(tag=the_tag)
                return redirect("all_articles")
        elif request.POST.get("status") == "add":
            list_tags = request.POST.get("tags")
            custom_data = QueryDict(mutable=True)
            custom_data.update(request.POST)
            custom_data.pop("tag", None)
            form = ArticleForm(request.POST)
            if form.is_valid():
                new_tag = form.cleaned_data["tag"]
                list_tags = list_tags.strip()
                list_tags = ast.literal_eval(list_tags)
                if new_tag != "":
                    try:
                        list_tags.index(new_tag)
                    except:
                        list_tags.append(new_tag)
            else:
                return HttpResponseForbidden()
            form = ArticleForm(custom_data)
        else:
            list_tags = request.POST.get("tags")
            the_tag = request.POST.get("delete")
            form = ArticleForm(request.POST)
            list_tags = list_tags.strip()
            list_tags = ast.literal_eval(list_tags)
            list_tags.remove(the_tag)
            try:
                delete_tag = get_article.tags.get(tag=the_tag)
                delete_tag.delete()
            except:
                pass
    else:
        form = ArticleForm(
            initial={"title": get_article.title, "article": get_article.article}
        )
        list_tags = [
            get_tag
            for get_tag in get_article.tags.values_list("tag", flat=True).distinct()
        ]
    len_tags = len(list_tags)
    return render(
        request,
        "articles/article_action.html",
        {"form": form, "list_tags": list_tags, "len_tags": len_tags},
    )


@login_required
def SpecificCreateView(request):
    if request.method == "POST":
        if request.POST.get("status") == "done":
            form = ArticleForm(request.POST)
            if form.is_valid():
                new_title = form.cleaned_data["title"]
                new_article = form.cleaned_data["article"]
                new_author = request.user
                the_article = Article.objects.create(
                    title=new_title, article=new_article, author=new_author
                )
                list_tags = request.POST.get("tags")
                list_tags = list_tags.strip()
                list_tags = ast.literal_eval(list_tags)
                for the_tag in list_tags:
                    Tag.objects.create(article=the_article, tag=the_tag)
                    if AllTags.objects.filter(tag=the_tag).exists() == False:
                        AllTags.objects.create(tag=the_tag)
                return redirect("all_articles")
        elif request.POST.get("status") == "add":
            list_tags = request.POST.get("tags")
            custom_data = QueryDict(mutable=True)
            custom_data.update(request.POST)
            custom_data.pop("tag", None)
            form = ArticleForm(request.POST)
            if form.is_valid():
                new_tag = form.cleaned_data["tag"]
                list_tags = list_tags.strip()
                list_tags = ast.literal_eval(list_tags)
                if new_tag != "":
                    try:
                        list_tags.index(new_tag)
                    except:
                        list_tags.append(new_tag)
            else:
                return HttpResponseForbidden()
            form = ArticleForm(custom_data)
        else:
            list_tags = request.POST.get("tags")
            the_tag = request.POST.get("delete")
            form = ArticleForm(request.POST)
            list_tags = list_tags.strip()
            list_tags = ast.literal_eval(list_tags)
            list_tags.remove(the_tag)
    else:
        form = ArticleForm()
        list_tags = []
    len_tags = len(list_tags)
    return render(
        request,
        "articles/article_action.html",
        {"form": form, "list_tags": list_tags, "len_tags": len_tags},
    )