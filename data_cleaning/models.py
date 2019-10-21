from django.db import models


class Contributor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    iswc = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    contributors = models.ManyToManyField(Contributor)

    def __str__(self):
        return self.title
