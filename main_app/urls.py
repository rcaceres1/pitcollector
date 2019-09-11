from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pits/', views.pits_index, name='index'),
    path('pits/<int:pit_id>/', views.pits_detail, name='detail'),
    path('pits/create/', views.PitCreate.as_view(), name='pits_create'),
    path('pits/<int:pk>/update/', views.PitUpdate.as_view(), name='pits_update'),
    path('pits/<int:pk>/delete/', views.PitDelete.as_view(), name='pits_delete'),
    path('pits/<int:pit_id>/add_feeding/', views.add_feeding, name='add_feeding'),
]