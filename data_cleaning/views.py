from rest_framework import viewsets

from data_cleaning.models import Song, Contributor
from data_cleaning.serializers import SongSerializer, ContributorSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint to see all Songs
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        iswc = self.request.query_params.get("iswc", None)
        if iswc:
            queryset = queryset.filter(iswc=iswc)
        return queryset


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint to see all Contributors
    """

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
