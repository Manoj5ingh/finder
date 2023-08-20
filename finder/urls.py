# from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
]
