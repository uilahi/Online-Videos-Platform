from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # AUTHENTICATION
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LogoutView.as_view(), name='logout'),

    #DASHBOARD
    path('dashboard', views.dashboard, name='dashboard'),

    #CREATE PAGE
    path('page/create', views.CreatePage.as_view(), name='create_page'),
    path('page/<int:pk>', views.DetailPage.as_view(), name='detail_page'),
    path('page/<int:pk>/update', views.UpdatePage.as_view(), name='update_page'),
    path('page/<int:pk>/delete', views.DeletePage.as_view(), name='delete_page')
]

