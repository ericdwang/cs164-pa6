from django.db.models import Avg
from django.db.models import Count

from senate.models import County


# USAGE:
# ./manage.py shell
# >>> execfile('queries.py')

print('Query 1')

counties = County.objects.filter(population_2010__gt=2000000) \
    .values('statecode', 'name', 'population_2010') \
    .order_by('-population_2010')

for county in counties:
    print('{}|{}|{}'.format(
        county['statecode'], county['name'], county['population_2010']))

print('\nQuery 2')

counties = County.objects.all() \
    .values('statecode') \
    .annotate(counties_per_state=Count('statecode')) \
    .order_by('counties_per_state')

for county in counties:
    print('{}|{}'.format(county['statecode'], county['counties_per_state']))

print('\nQuery 3')

avg_counties = County.objects.all() \
    .values('statecode') \
    .annotate(counties_per_state=Count('statecode')) \
    .aggregate(avg_counties=Avg('counties_per_state')) \
    .values()[0]

print(avg_counties)
