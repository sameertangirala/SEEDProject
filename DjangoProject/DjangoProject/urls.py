from django.contrib import admin
from django.urls import path, include
from django_cas_ng import views as cas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('links.urls')),
    path('accounts/login/', cas_views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path('accounts/callback/', cas_views.CallbackView.as_view(), name='cas_ng_callback'),
]
