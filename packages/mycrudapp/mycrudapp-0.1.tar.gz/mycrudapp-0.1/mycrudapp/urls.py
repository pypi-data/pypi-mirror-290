from django.urls import path
from .views import MyModelListCreateView, MyModelRetrieveUpdateDestroyView

urlpatterns = [
    path('mymodel/', MyModelListCreateView.as_view(), name='mymodel-list-create'),
    path('mymodel/<int:pk>/', MyModelRetrieveUpdateDestroyView.as_view(), name='mymodel-rud'),
]
