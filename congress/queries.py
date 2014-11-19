from django.db.models import Avg
from django.db.models import Count
from django.db.models import Max
from django.db.models import Q
from django.db.models import F
from django.db.models import Sum

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

print(counties.query)
print('')

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

print(counties.query)
print('')

for county in counties:
    print('{}|{}'.format(county['statecode'], county['counties_per_state']))

##############################################################################
print('\nQuery 3')
##############################################################################

avg_counties = County.objects.all() \
    .values('statecode') \
    .annotate(counties_per_state=Count('statecode')) \

print(avg_counties.query)
print('')

avg_counties = avg_counties.aggregate(avg_counties=Avg('counties_per_state')) \
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

print(count_states_more_than_avg.query)
print('')

count_states_more_than_avg =  count_states_more_than_avg.count()

print(count_states_more_than_avg)

##############################################################################
print('\nQuery 5')
##############################################################################

# I don't think it's possible in the Django ORM to cleanly reference
# a 'parent' query in a subquery, as we do in the SQL for this query.
'''
states = State.objects.exclude(population_2010=
    County.objects.filter(statecode=CURRENT_STATE) \
        .values('population_2010') \
        .aggregate(total_population=Sum('population_2010')) \
        .values()[0]
    )
'''

states = []
for state in State.objects.all():
    total_population = County.objects.filter(statecode=state) \
        .values('population_2010') \
        .aggregate(total_population=Sum('population_2010')) \
        .values()[0]
    if total_population != state.population_2010:
        states.append(state.statecode)

for state in states:
    print(state)

##############################################################################
print('\nQuery 6')
##############################################################################

num_jon = Senator.objects \
    .filter(Q(name__startswith='John') | Q(name__startswith='Jon')) \
    .values('statecode') \
    .distinct() \

print(num_jon.query)
print('')

num_jon = num_jon.count()

print(num_jon)

##############################################################################
print('\nQuery 7')
##############################################################################

# This isn't possible without casting in the database...
# However, the ORM doesn't really let us cast on a key in a foreign table,
# so there's no real way to do this.
print('Unimplemented')

# This is what it would look like if we could access foreign key fields in
# an extra statement
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

# This is the version that does comparisons on the uncasted date string
'''
sen_list = Senator.objects \
    .select_related() \
    .values('statecode', 'statecode__admitted_to_union', 'name', 'born') \
    .filter(born__lt=F('statecode__admitted_to_union')) \
    .values('statecode', 'statecode__admitted_to_union', 'name', 'born')


for sen in sen_list:
    print('{}|{}|{}|{}'.format(sen['statecode'], sen['statecode__admitted_to_union'], \
        sen['name'], sen['born']))
'''

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

print(wv_counties.query)
print('')

for county in wv_counties:
    print('{}|{}'.format(county['name'], county['pop_diff']))

##############################################################################
print('\nQuery 9')
##############################################################################

num_chairmen = Committee.objects \
    .select_related() \
    .values('chairman__statecode') \
    .annotate(pop_sum=Count('chairman__statecode'))

max_chairmen = num_chairmen \
    .aggregate(max_pop=Max('pop_sum')) \
    .values()[0]

states_with_max = num_chairmen \
    .filter(pop_sum__gte=max_chairmen) \
    .values('chairman__statecode')

print(states_with_max.query)
print('')

for state in states_with_max:
    print('{}'.format(state['chairman__statecode']))

##############################################################################
print('\nQuery 10')
##############################################################################

st_with_chairmen = Committee.objects \
    .select_related('chairman') \
    .values('chairman__statecode')

st_without_chairmen = State.objects.all() \
    .exclude(statecode__in=st_with_chairmen) \
    .values('statecode')

print(st_without_chairmen.query)
print('')

for state in st_without_chairmen:
    print('{}'.format(state['statecode']))

##############################################################################
print('\nQuery 11')
##############################################################################

sc_same_chairman = Committee.objects \
    .select_related('chairman', 'parent_committee') \
    .filter(parent_committee__chairman__exact=F('chairman')) \
    .values('parent_committee__id', 'parent_committee__chairman', \
        'id', 'chairman')

print(sc_same_chairman.query)
print('')

for sc in sc_same_chairman:
    print('{}|{}|{}|{}'.format(sc['parent_committee__id'], sc['parent_committee__chairman'], \
        sc['id'], sc['chairman']))

##############################################################################
print('\nQuery 12')
##############################################################################

sc_earlier_birth = Committee.objects \
    .select_related('chairman', 'parent_committee') \
    .select_related('parent_committee__chairman') \
    .filter(parent_committee__chairman__born__gt=F('chairman__born')) \
    .values('parent_committee__id', 'parent_committee__chairman', \
        'parent_committee__chairman__born', 'id', 'chairman', \
        'chairman__born')

print(sc_earlier_birth.query)
print('')

for sc in sc_earlier_birth:
    print('{}|{}|{}|{}|{}|{}'.format(sc['parent_committee__id'], \
        sc['parent_committee__chairman'], sc['parent_committee__chairman__born'], \
        sc['id'], sc['chairman'], sc['chairman__born']))

##############################################################################
print('\nQuery 13')
##############################################################################

County.objects.create(
    name='Berkeley', statecode=State.objects.get(statecode='CA'),
    population_1950=113805, population_2010=112580)
for county in County.objects.filter(name='Berkeley'):
    print(county.statecode.statecode)

##############################################################################
print('\nQuery 14')
##############################################################################

County.objects.get(
    name='Berkeley', statecode=State.objects.get(statecode='CA')).delete()
for county in County.objects.filter(name='Berkeley'):
    print(county.statecode.statecode)
