from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pits/', views.pits_index, name='index'),
    path('pits/<int:pit_id>/', views.pits_detail, name='detail'),
    path('cats/create/', views.PitCreate.as_view(), name='pits_create'),
    path('cats/<int:pk>/update/', views.PitUpdate.as_view(), name='pits_update'),
    path('cats/<int:pk>/delete/', views.PitDelete.as_view(), name='pits_delete'),
]