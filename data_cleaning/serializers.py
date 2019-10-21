"""
Serializers for Django Rest Framework
"""

from rest_framework import serializers

from data_cleaning.models import Song, Contributor


class ContributorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contributor
        fields = ["name"]


class SongSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Song
        fields = ["iswc", "title", "contributors"]
