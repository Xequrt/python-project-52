from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, login_view, logout_view

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]