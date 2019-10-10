from django.contrib import admin
from django.urls import path, include
from django.conf import settings          
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve  #追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)