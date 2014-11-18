from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class State(models.Model):
    statecode = models.CharField(max_length=2, primary_key=true)
    population_2010 = models.IntegerField()
    population_2000 = models.IntegerField()
    population_1950 = models.IntegerField()
    population_1900 = models.IntegerField()
    landarea = models.FloatField()
    name = models.CharField(max_length=50)
    admitted_to_union = models.CharField(max_length=50)

class County(models.Model):
    name = models.CharField(max_length=50)
    statecode = models.ForeignKey(State, to_field='statecode')
    population_1950 = models.IntegerField()
    population_2010 = models.IntegerField()

class Senator(models.Model):
    statecode = models.ForeignKey(State, to_field='statecode')
    name = models.CharField(max_length=100, primary_key=true)
    affiliation = models.CharField(max_length=100)
    took_office = models.IntegerField()
    born = models.IntegerField()

class Committee(models.Model):
    id = models.CharField(max_length=100, primary_key=true)
    parent_committee = models.ForeignKey(Committee, to_field='id')
    name = models.CharField(max_length=100)
    chairman = models.ForeignKey(Senator, to_field='name')
    ranking_member = models.ForeignKey(Senator, to_field='name')
