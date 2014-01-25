from django.db import models


class Candidate(models.Model):
    """
    A candidate for Los Angeles Mayor
    """
    first_name = models.CharField(max_length=800)
    last_name = models.CharField(max_length=800)
    objects = models.Manager()


class Committee(models.Model):
    """
    An independent campaign committee for a mayoral candidate
    """
    name = models.CharField(max_length=1000)
    committee_id = models.IntegerField()
    MayoralCandidate2012 = models.ForeignKey("Candidate")
    objects = models.Manager()


class Contribution(models.Model):
    """
    An individual contribution to a mayoral campaign
    """
    MayoralCandidate2012 = models.ForeignKey("Candidate", null=True, blank=True)
    MayoralCommittee2012 = models.ForeignKey("Committee", null=True, blank=True)
    CONTRIB_TYPE_CHOICES = (('independent', 'independent'), ('candidate', 'candidate'))
    contrib_type = models.CharField(max_length=800, choices=CONTRIB_TYPE_CHOICES)
    ELECTION_CHOICES = (('primary', 'primary'), ('general', 'general'))
    election = models.CharField(max_length=800, choices=CONTRIB_TYPE_CHOICES, blank=True)
    city = models.CharField(max_length=800, blank=True)
    state = models.CharField(max_length=800, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    first_name = models.CharField(max_length=800, blank=True)
    last_name = models.CharField(max_length=800, blank=True)
    race = models.CharField(max_length=800, blank=True)
    occupation = models.CharField(max_length=800, blank=True)
    employer = models.CharField(max_length=800, blank=True)
    lat_employer = models.CharField(max_length=800, blank=True)
    sector = models.CharField(max_length=800, blank=True)
