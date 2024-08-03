from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf.urls.static import static
from library_management import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'homepage'),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('category/<slug:book_slug>/', home, name = 'category_wise_books'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
