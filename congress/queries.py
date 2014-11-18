from senate.models import County


# USAGE:
# ./manage.py shell
# >>> execfile('queries.py')

print(' ')
print('Query 1')

counties = County.objects.filter(
    population_2010__gt=2000000).values(
        'statecode', 'name', 'population_2010').order_by('-population_2010')
for county in counties:
    print('{}|{}|{}'.format(
        county['statecode'], county['name'], county['population_2010']))
