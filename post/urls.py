from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
]