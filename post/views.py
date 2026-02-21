from django.shortcuts import render
from post.models import Post
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F

from .models import Post

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class PostListView(ListView):
    model = Post
    template_name = 'post/posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return (
            Post.objects
            .select_related('user', 'category')
            .order_by('-created')
        )



class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # 🔥 views_count ni atomik oshirish
        Post.objects.filter(pk=obj.pk).update(
            views_count=F('views_count') + 1
        )
        obj.refresh_from_db()

        return obj

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_form.html'
    fields = ['title', 'content', 'image', 'video', 'category']
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_form.html'
    fields = ['title', 'content', 'image', 'video', 'category']
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.slug})



class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('post-list')


def home_view(request):
    posts = Post.objects.all()[:8]
    return render(request, 'pages/home.html', {'posts': posts})