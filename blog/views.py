from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from post.models import Post
from .models import Like, Wishlist


@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'post-list'))


@login_required
def toggle_wishlist(request, slug):
    post = get_object_or_404(Post, slug=slug)

    wish, created = Wishlist.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        wish.delete()

    return redirect(request.META.get('HTTP_REFERER', 'post-list'))

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Wishlist


@login_required
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('post', 'post__user')

    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'blog/wishlist.html', context)