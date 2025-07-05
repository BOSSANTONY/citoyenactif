from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('signalement/nouveau/', views.signalement_create, name='signalement_nouveau'),
    path('mes-signalements/', views.mes_signalements, name='mes_signalements'),
    path('carte/', views.carte, name='carte'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ma-carte/', views.ma_carte, name='ma_carte'),
    path('carte-utilisateur/<int:user_id>/', views.carte_utilisateur, name='carte_utilisateur'),
    path('supprimer-signalement/<int:signalement_id>/', views.supprimer_signalement, name='supprimer_signalement'),
    path('supprimer-utilisateur/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),

]
