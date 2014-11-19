from django.db.models import Avg
from django.db.models import Count
from django.db.models import Q
from django.db.models import F

from senate.models import County
from senate.models import Senator
from senate.models import State
from senate.models import Committee


# USAGE:
# ./manage.py shell
# >>> execfile('queries.py')

##############################################################################
print('Query 1')
##############################################################################

counties = County.objects.filter(population_2010__gt=2000000) \
    .values('statecode', 'name', 'population_2010') \
    .order_by('-population_2010')

for county in counties:
    print('{}|{}|{}'.format(
        county['statecode'], county['name'], county['population_2010']))

##############################################################################
print('\nQuery 2')
##############################################################################

counties = County.objects.all() \
    .values('statecode') \
    .annotate(counties_per_state=Count('statecode')) \
    .order_by('counties_per_state')

for county in counties:
    print('{}|{}'.format(county['statecode'], county['counties_per_state']))

##############################################################################
print('\nQuery 3')
##############################################################################

avg_counties = County.objects.all() \
    .values('statecode') \
    .annotate(counties_per_state=Count('statecode')) \
    .aggregate(avg_counties=Avg('counties_per_state')) \
    .values()[0]

print(avg_counties)

##############################################################################
print('\nQuery 4')
##############################################################################

avg_counties = County.objects.all() \
    .values('statecode') \
    .annotate(counties_per_state=Count('statecode')) \
    .aggregate(avg_counties=Avg('counties_per_state')) \
    .values()[0]

count_states_more_than_avg = County.objects.all() \
    .values('statecode') \
    .annotate(num_state=Count('statecode')) \
    .filter(num_state__gt=avg_counties) \
    .count()

print(count_states_more_than_avg)

##############################################################################
print('\nQuery 5')
##############################################################################

# I don't think it's possible in the Django ORM to cleanly reference
# a 'parent' query in a subquery, as we do in the SQL for this query.
print('Unimplemented')

##############################################################################
print('\nQuery 6')
##############################################################################

num_jon = Senator.objects \
    .filter(Q(name__startswith='John') | Q(name__startswith='Jon')) \
    .values('statecode') \
    .distinct() \
    .count()

print(num_jon)

##############################################################################
print('\nQuery 7')
##############################################################################

# This isn't possible without casting in the database...
# However, the ORM doesn't really let us cast on a key in a foreign table,
# so there's no real way to do this.

'''
sen_list1 = Senator.objects \
    .select_related() \
    .extra( select={'admit_year': "cast(strftime('%Y',statecode__admitted_to_union) as integer)"}) 
print(sen_list1)

sen_list = sen_list1 \
    .values('statecode', 'admit_year', 'name', 'born') \
    .filter(born__lt=F('admit_year')) \
    .values('statecode', 'admit_year', 'name', 'born')

'''


sen_list = Senator.objects \
    .select_related() \
    .values('statecode', 'statecode__admitted_to_union', 'name', 'born') \
    .filter(born__lt=F('statecode__admitted_to_union')) \
    .values('statecode', 'statecode__admitted_to_union', 'name', 'born')


for sen in sen_list:
    print('{}|{}|{}|{}'.format(sen['statecode'], sen['statecode__admitted_to_union'], \
        sen['name'], sen['born']))

##############################################################################
print('\nQuery 8')
##############################################################################

# This can't be done properly, since you can't return a difference between
# fields without calling extra.

wv_counties = County.objects \
    .select_related() \
    .filter(statecode__exact="WV") \
    .filter(population_1950__gt=F('population_2010')) \
    .extra( select={'pop_diff':'population_1950 - population_2010'}) \
    .values('name', 'pop_diff')

for county in wv_counties:
    print('{}|{}'.format(county['name'], county['pop_diff']))

##############################################################################
print('\nQuery 9')
##############################################################################


##############################################################################
print('\nQuery 10')
##############################################################################


##############################################################################
print('\nQuery 11')
##############################################################################


##############################################################################
print('\nQuery 12')
##############################################################################


