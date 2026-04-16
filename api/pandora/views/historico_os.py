from rest_framework import viewsets
from pandora.models import HistoricoOS
from pandora.serializers import HistoricoOSSerializer

class HistoricoOSViewSet(viewsets.ModelViewSet):
    queryset = HistoricoOS.objects.all()
    serializer_class = HistoricoOSSerializer