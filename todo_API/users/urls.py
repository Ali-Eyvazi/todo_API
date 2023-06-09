from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import views

urlpatterns = [
        path('register/',views.RegisterView.as_view(),name='register'),
        path('login/', TokenObtainPairView.as_view(), name='login'),
        path('refresh/', TokenRefreshView.as_view(), name='refreshtoken'),
        path('logout/', views.LogoutView.as_view(), name='refreshtoken'),

]
