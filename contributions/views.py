import json
from django.db.models import Sum, Count
from django.views.generic import TemplateView
from contributions.models import Contribution

#
# This is a Django Class-based view...
# To read more about what's going on, head here:
# https://docs.djangoproject.com/en/dev/topics/class-based-views/
#
# Pro tip:
#
# If you want to feed your data into a JavaScript charting
# library like D3, you may need to transform it into Python
# lists or a dictionary.
#
# Get your data formatted the way you need it, then use
# the json module to serialize your data and pass it to the
# template:
#
# context['my_data'] = json.dumps({"key": "value"})
#


class IndexView(TemplateView):
    # tell our view which template to use
    template_name = "contributions/index.html"

    # We're going to override the default method to get the
    # context for our template, so we can add a bunch of
    # custom data.
    def get_context_data(self, **kwargs):
        # grab our existing context dictionary, so we can add to it.
        # If 'super' is confusing, the docs are here:
        # http://docs.python.org/2/library/functions.html#super
        context = super(IndexView, self).get_context_data(**kwargs)
        
        # First, let's get the contributions for each candidate
        # For more on Django querysets, head here:
        # https://docs.djangoproject.com/en/1.6/ref/models/querysets/
        garcetti_contributions = Contribution.objects.filter(candidate__last_name='Garcetti')
        greuel_contributions = Contribution.objects.filter(candidate__last_name='Greuel')

        # Next, we can add the total amount for each to the context
        # using Django's built in Sum aggregation method.
        # You can find out more here: https://docs.djangoproject.com/en/1.6/topics/db/aggregation/
        context['garcetti_total'] = garcetti_contributions.aggregate(Sum('amount'))['amount__sum']
        context['greuel_total'] = greuel_contributions.aggregate(Sum('amount'))['amount__sum']

        # Now that we have the totals, let's get the breakdown for
        # direct and independent contributions
        context['garcetti_independent'] = garcetti_contributions.filter(
            contrib_type='independent'
        ).aggregate(Sum('amount'))['amount__sum']
        
        context['garcetti_direct'] = garcetti_contributions.filter(
            contrib_type='candidate'
        ).aggregate(Sum('amount'))['amount__sum']

        context['greuel_independent'] = greuel_contributions.filter(
            contrib_type='independent'
        ).aggregate(Sum('amount'))['amount__sum']
        
        context['greuel_direct'] = greuel_contributions.filter(
            contrib_type='candidate'
        ).aggregate(Sum('amount'))['amount__sum']

        # Let's also grab the contributions by sector
        sectors = set(Contribution.objects.all().values_list('sector', flat=True))
        # You can print out variables to help debug. Check your console...
        print sectors

        # We're going to generate some lists with everything in them now,
        # then refine the data in our loop below, to save multiple
        # database hits on each iteration.
        all_sectors = Contribution.objects.values_list('sector', 'amount')
        garcetti_sectors = garcetti_contributions.values_list('sector', 'amount')
        greuel_sectors = greuel_contributions.values_list('sector', 'amount')

        # we'll set up an empty list here, then add to it
        # as we iterate through our sectors and compute the totals.
        contributions_by_sector = []

        # Python list comprehensions are amazing. Learn more:
        # http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
        for sector in sectors:
            contributions_by_sector.append({
                'name': sector,
                'garcetti': sum([i[1] for i in garcetti_sectors if i[0] == sector]),
                'greuel': sum([i[1] for i in greuel_sectors if i[0] == sector]),
                'total': sum([i[1] for i in all_sectors if i[0] == sector]),
            })

        # for more info on this sort, check out:
        #   https://wiki.python.org/moin/HowTo/Sorting
        contributions_by_sector = sorted(contributions_by_sector,
                                    key=lambda k: k['total'], reverse=True) 

        # Now that we've got the data, add it to the context
        context['contributions_by_sector'] = contributions_by_sector
        # return the amended context to the template
        return context

