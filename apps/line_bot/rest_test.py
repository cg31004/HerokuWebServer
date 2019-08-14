from rest_framework import viewsets, serializers, permissions
from .models import TheaterModel
from rest_framework import mixins,routers

class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterModel
        fields = ("theater_name","theater_area","theater_address",)

class TheaterViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    model = TheaterModel

v1 = routers.DefaultRouter()
v1.register(r'store', TheaterViewSet)
v1.register(r'stores/Theater', TheaterViewSet)