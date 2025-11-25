from django.urls import path
from . import views
from .views import principal_delete

urlpatterns = [
    path('principals/', views.principal_list, name='principal_list'),
    path('principals/add/', views.principal_add, name='principal_add'),
    path('principals/<int:pk>/', views.principal_detail, name='principal_detail'),
    path('principals/<int:pk>/edit/', views.principal_edit, name='principal_edit'),
    path('principals/<int:pk>/delete/', principal_delete, name='principal_delete'),

]
