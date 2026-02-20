from django.db import models
from user.models import CustomUser
from post.models import Post
class Comment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='posts')
    created_at=models.DateTimeField(auto_now_add=True)
    text=models.TextField()


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    title=models.CharField(max_length=200,null=True,blank=True)
    participants=models.ManyToManyField(CustomUser,related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Messages(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='message')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='message')
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='chat')
