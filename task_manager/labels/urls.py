from django.urls import path
from .views import LabelsListView, LabelsCreateView, LabelsUpdateView, LabelsDeleteView

urlpatterns = [
    path('', LabelsListView.as_view(), name='labels_list'),
    path('create/', LabelsCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelsUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelsDeleteView.as_view(), name='label_delete'),
]