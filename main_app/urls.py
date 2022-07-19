from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('fighters/', views.game_index, name = 'index'),
    path('fighters/<int:game_id>/', views.game_detail, name = 'detail'),
    path('fighters/create', views.GamesCreate.as_view(), name='game_create'),
    path('fighters/<int:pk>/update/', views.GamesUpdate.as_view(), name='game_update'),
    path('fighters/<int:pk>/delete/', views.GamesDelete.as_view(), name='game_delete'),
    path('fighters/<int:game_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]