from django.shortcuts import render
from .models import Post
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.db.models.query import QuerySet


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'main.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'article'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostCreate(CreateView):
    #permission_required = 'newsapp.add_news'
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post=form.save(commit=False)
        if self.request.path=='/news/article/create/':
            post.postCategory = 'AR'
        post.save()
        return super().form_valid(form)

class PostEdit(UpdateView):
    # permission_required = ('newsapp.change_news',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

class PostDelete(DeleteView):
    # permission_required = ('newsapp.delete_news',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')
