from django.db import models
from django.utils.text import slugify
from user.models import CustomUser
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    name=models.CharField(max_length=100)
    desc=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=200)
    slug = models.SlugField(unique=True,null=True, blank=True, max_length=255)
    user=models.ForeignKey(CustomUser,
                           on_delete=models.CASCADE,
                           related_name='auth_posts')
    content=models.TextField()
    image=models.ImageField(upload_to='post_images',null=True,blank=True)
    video=models.FileField(upload_to='post_video/',
                           validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'wmv'])],
                           null=True,
                           blank=True)
    category=models.ForeignKey(Category,
                               on_delete=models.SET_NULL,
                               null=True,blank=True,
                               related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    views_count=models.PositiveIntegerField(default=0)
    allow_comments = models.BooleanField(default=True, verbose_name="Izohga ruxsat")

    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)




