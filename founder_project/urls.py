from django.contrib import admin
from django.urls import path, include
import products.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('', products.views.homepage, name='home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
