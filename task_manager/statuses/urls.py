from django.urls import path
from .views import StatusesListView, StatusesCreateView, StatusesUpdateView, StatusesDeleteView

urlpatterns = [
    path('', StatusesListView.as_view(), name='statuses_list'),
    path('create/', StatusesCreateView.as_view(), name='statuses_create'),
    path('<int:pk>/update/', StatusesUpdateView.as_view(), name='statuses_update'),
    path('<int:pk>/delete/', StatusesDeleteView.as_view(), name='statuses_delete'),
]