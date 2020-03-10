from django.urls import path
from .views import (home ,  )

urlpatterns = [
    #path('detail/<int:pk>/', CityDetailView.as_view() , name='detail'),
    #path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    #path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
    #path('add/', CityCreateView.as_view(), name='add'),
    path('', home, name='home'),

]
