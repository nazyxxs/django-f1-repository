# Підключає маршрути додатку f1
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('f1.urls')),  # ← наш REST API
    path('frontend/', include('frontend.urls')),
    path('', include('f1.urls')),
]
