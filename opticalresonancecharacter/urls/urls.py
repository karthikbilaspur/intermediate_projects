from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('display/<pk>/', views.display_text, name='display_text'),
    path('edit/<pk>/', views.edit_text, name='edit_text'),
    path('history/', views.history, name='history'),
    path('download/<pk>/', views.download_text, name='download_text'),
    path('download_pdf/<pk>/', views.download_pdf, name='download_pdf'),
]