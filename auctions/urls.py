from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name='create'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('categories/all', views.categories_all, name='categories'), 
    path('categories/<str:category>', views.category, name='category'), 
    path('listing/<str:item>', views.listing, name='listing')
]
