from rest_framework import viewsets
from datasets.models import datasets
from datasets.serializers import datasetsSerializer

class datasetsViewSet(viewsets.ModelViewSet):
    # from scripts import import_datasets
    # import_datasets.add_data()
    queryset = datasets.objects.all()
    serializer_class = datasetsSerializer
