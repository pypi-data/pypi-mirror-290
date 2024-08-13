from rest_framework import serializers
from .models import CrudModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrudModel
        fields = '__all__'
