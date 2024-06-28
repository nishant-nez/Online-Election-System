from django.contrib import admin
from .models import Election, Candidate, Vote, Result

admin.site.register([Election, Candidate, Vote, Result])