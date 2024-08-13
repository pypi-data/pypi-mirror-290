from rest_framework import generics
from .models import CrudModel
from .serializers import MyModelSerializer

class MyModelListCreateView(generics.ListCreateAPIView):
    queryset = CrudModel.objects.all()
    serializer_class = MyModelSerializer

class MyModelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrudModel.objects.all()
    serializer_class = MyModelSerializer
