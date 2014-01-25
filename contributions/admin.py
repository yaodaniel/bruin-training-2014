from django.contrib import admin
from contributions.models import Candidate, Committee, Contribution

admin.site.register(Candidate)
admin.site.register(Committee)
admin.site.register(Contribution)