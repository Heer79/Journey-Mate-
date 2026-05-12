from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages_list, name='packages_list'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
]
