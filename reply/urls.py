from django.urls import path

from . import views

urlpatterns=[
    path('repl-comment/<int:comment_id>',views.ReplyComment.as_view(),name='reply_comment_page'),
    path('comment/update/<int:comment_id>/',views.CommentUpdate.as_view(),name='comment_update'),
    path('comment/delete/<int:comment_id>/',views.CommentDelete.as_view(),name='comment_delete'),
    path('chat/<int:chat_id>/', views.ChatDetail.as_view(), name='chat_detail'),
    path('start-chat/<int:recipient_id>/', views.ChatCreate.as_view(), name='start_chat'),
    path('message-update/<int:message_id/>',views.MessageUpdate.as_view(),name='message-update'),
    path('message-delete/<int:message_id/>',views.MessageDelete.as_view(),name='message-delete'),
]