from django.db import models


class State(models.Model):
    statecode = models.TextField(primary_key=True)
    population_2010 = models.IntegerField()
    population_2000 = models.IntegerField()
    population_1950 = models.IntegerField()
    population_1900 = models.IntegerField()
    landarea = models.FloatField()
    name = models.TextField()
    admitted_to_union = models.TextField()


class County(models.Model):
    name = models.TextField()
    statecode = models.ForeignKey(State)
    population_1950 = models.IntegerField()
    population_2010 = models.IntegerField()


class Senator(models.Model):
    name = models.TextField(primary_key=True)
    statecode = models.ForeignKey(State)
    affiliation = models.TextField()
    took_office = models.IntegerField()
    born = models.IntegerField()


class Committee(models.Model):
    id = models.TextField(primary_key=True)
    parent_committee = models.ForeignKey('self')
    name = models.TextField()
    chairman = models.ForeignKey(Senator)
    ranking_member = models.ForeignKey(Senator)
