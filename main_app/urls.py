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
    path('pits/<int:pit_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('pits/<int:pit_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('pits/<int:pit_id>/add_photo/', views.add_photo, name='add_photo'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('accounts/signup', views.signup, name='signup'),
]