from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Election(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='election_pics/default.jpg', upload_to='election_pics')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.end_date <= timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id) +  ' - ' + self.title



class Candidate(models.Model):
    gender_choices = {
        ('male', 'Male'),
        ('female', 'Female'),
    }

    name = models.CharField(max_length=100)
    description = models.TextField()
    dob = models.DateField()
    gender = models.CharField(choices=gender_choices, max_length=6)
    image = models.ImageField(default='candidate_pics/default.jpg', upload_to='candidate_pics')
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.name



class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('election', 'voter')

    def __str__(self):
        return str(self.id) + ' - ' + self.election.title + ' - ' + self.voter.username + ' for ' + self.candidate.name



class Result(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id) + ' - ' + self.election.title + ' - ' + self.candidate.name

