import os
import csv
import logging
import datetime
import statestyle
from django.conf import settings
from contributions.models import Candidate, Committee, Contribution
from django.core.management.base import BaseCommand, CommandError
logger = logging.getLogger(__name__)

data_path = os.path.join(settings.ROOT_PATH, 'contributions', 'data')


class Command(BaseCommand):
    help = 'A management command to load in some CSV data for the LA mayoral contributions.'

    def clean_amount(self, amount):
        if amount == '':
            return None
        
        raw = amount.replace('$', '').replace(',', '').strip()
        try:
            return int(raw)
        except ValueError:
            return float(raw)
        except:
            logger.debug('Messed up value: %s' % amount)
            return None
    
    def clean_date(self, date):
        """
        converts a date formatted like 20120101 into a python datetime.date object
        """
        try:
            return datetime.datetime.strptime(date, '%m/%d/%Y').date()
        except ValueError:
            return None

    def clean_state(self, state):
        try:
            obj = statestyle.get(state)
            return obj.postal
        except ValueError:
            return ''

    def clean_election(self, election):
        if 'primary' in election.lower():
            return 'primary'
        elif 'general' in election.lower():
            return 'general'
        else:
            return ''

    def clean_sector(self, sector):
        return sector.strip().title()
    
    def load_independent_contribs(self, garcetti, greuel):
        """
        Load in the contributions to individual candidates
        """
        logger.debug('Cracking open independent_contribs.csv')
        data_file = open(os.path.join(data_path, 'independent_contribs.csv'), 'rU')
        rdr = csv.DictReader(data_file)
        for i in rdr:
            cand = i.get('candidate', '').lower()
            if cand in ['garcetti', 'greuel']:

                if cand == 'garcetti':
                    candidate = garcetti
                
                if cand == 'greuel':
                    candidate = greuel
                
                committee, created = Committee.objects.get_or_create(
                    name=i.get('committee', ''),
                    committee_id=self.clean_amount(i.get('Committee ID', '')),
                    candidate=candidate,
                )

                if created:
                    logger.debug('Created commitee %s' % committee.name)

                Contribution.objects.create(
                    committee=committee,
                    candidate=candidate,
                    contrib_type='independent',
                    city=i.get('city', ''),
                    state=self.clean_state(i.get('state', '')),
                    zip_code=self.clean_amount(i.get('zip', None)),
                    date=self.clean_date(i.get('date', None)),
                    amount=i.get('amount', None).replace(',',''),
                    first_name=i.get('first', ''),
                    last_name=i.get('last', ''),
                    race='Mayor',
                    occupation=i.get('occupation', ''),
                    employer=i.get('employer', ''),
                    election=self.clean_election(i.get('election', '')),
                    lat_employer=i.get('LATemployer', ''),
                    sector=self.clean_sector(i.get('sector', '')),
                )
        
        logger.debug('Created %s mayoral contribs' % Contribution.objects.filter(contrib_type='independent').count())

    def load_candidate_contribs(self, garcetti, greuel):
        """
        Load in the contributions to individual candidates
        """
        logger.debug('Cracking open candidate_contribs.csv')
        data_file = open(os.path.join(data_path, 'candidate_contribs.csv'), 'rU')
        rdr = csv.DictReader(data_file)
        for i in rdr:
            cand = i.get('candidate', '').strip().lower()
            if cand in ['garcetti', 'greuel']:
                
                if cand == 'garcetti':
                    candidate = garcetti
                
                if cand == 'greuel':
                    candidate = greuel
                
                Contribution.objects.create(
                    candidate=candidate,
                    contrib_type='candidate',
                    city=i.get('city', ''),
                    state=self.clean_state(i.get('state', '')),
                    zip_code=self.clean_amount(i.get('zip', None)),
                    date=self.clean_date(i.get('date', None)),
                    amount=i.get('amount', None),
                    first_name=i.get('first', ''),
                    last_name=i.get('last', ''),
                    race=i.get('race', ''),
                    occupation=i.get('occupation', ''),
                    employer=i.get('employer', ''),
                    lat_employer=i.get('LATemployer', ''),
                    sector=self.clean_sector(i.get('sector', '')),
                    election=self.clean_election(i.get('election', '')),
                )
        
        logger.debug('Created %s mayoral contribs' % Contribution.objects.filter(contrib_type='candidate').count())
   
    def load_ie_expends(self, garcetti, greuel):
        """
        Load in the contributions to individual candidates
        """
        logger.debug('Cracking open ie_spending.csv')
        data_file = open(os.path.join(data_path, 'ie_spending.csv'), 'rU')
        rdr = csv.DictReader(data_file)
        for i in rdr:
            cand = i.get('candidate', '').strip().lower()
            if cand in ['garcetti', 'greuel']:
                
                if cand == 'garcetti':
                    candidate = garcetti
                
                if cand == 'greuel':
                    candidate = greuel
                Contribution.objects.create(
                    candidate=candidate,
                    contrib_type='independent',
                    city=i.get('city', ''),
                    state=self.clean_state(i.get('state', '')),
                    zip_code=self.clean_amount(i.get('zip', None)),
                    date=self.clean_date(i.get('date', None)),
                    amount=i.get('amount', None),
                    first_name=i.get('first', ''),
                    last_name=i.get('last', ''),
                    race=i.get('race', ''),
                    occupation=i.get('occupation', ''),
                    employer=i.get('employer', ''),
                    lat_employer=i.get('LATemployer', ''),
                    sector=self.clean_sector(i.get('sector', '')),
                    election=self.clean_election(i.get('election', '')),
                )
        
        # logger.debug('Created %s mayoral contribs' % Contribution.objects.filter(contrib_type='candidate').count())

    def handle(self, *args, **options):
        # Clear out all the old cruft
        Contribution.objects.all().delete()
        # If we don't have Garcetti in the database make him
        garcetti, created = Candidate.objects.get_or_create(
            first_name = "Eric",
            last_name = "Garcetti",
        )
        if created:
            logger.debug('Created mayoral candidate %s %s' % (garcetti.first_name, garcetti.last_name))
        # Same for Greuel
        gruel, created = Candidate.objects.get_or_create(
            first_name = "Wendy",
            last_name = "Greuel",
        )
        if created:
            logger.debug('Created mayoral candidate %s %s' % (gruel.first_name, gruel.last_name))        
        # load in our individual candidate contributions
        self.load_candidate_contribs(garcetti, gruel)
        self.load_independent_contribs(garcetti, gruel)
        self.load_ie_expends(garcetti, gruel)