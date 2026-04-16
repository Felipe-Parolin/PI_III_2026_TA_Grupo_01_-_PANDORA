from rest_framework import viewsets
from pandora.models import AnexoOS
from pandora.serializers import AnexoOSSerializer

class AnexoOSViewSet(viewsets.ModelViewSet):
    queryset = AnexoOS.objects.all()
    serializer_class = AnexoOSSerializer