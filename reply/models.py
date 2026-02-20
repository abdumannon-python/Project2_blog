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
    participants=models.ManyToManyField(CustomUser,related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_recipient(self, current_user):
        return self.participants.exclude(id=current_user.id).first()
    def last_message(self):
        return self.messages.all().last()

class Messages(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_message')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True,related_name='shared_posts')
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='message_images',null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering=['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

