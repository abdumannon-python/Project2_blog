
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),
    path('post/',include('post.urls')),
    path('reply/',include('reply.urls')),
    path('user/',include('user.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
