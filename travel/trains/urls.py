from django.urls import path
from .views import (home, TrainCreateView, TrainDeleteView, TrainDetailView,TrainUpdateView )

urlpatterns = [
    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),
    path('add/', TrainCreateView.as_view(), name='add'),
    path('', home, name='home'),

]
