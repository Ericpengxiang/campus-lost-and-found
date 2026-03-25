from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.MeView.as_view(), name='me'),
    path('me/unread/', views.unread_count, name='unread_count'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('admin/list/', views.AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
]
