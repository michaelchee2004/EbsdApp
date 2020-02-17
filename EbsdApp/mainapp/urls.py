from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('input', views.input_page, name='input_page'),
    path('run', views.run_page, name='run_page')
]
