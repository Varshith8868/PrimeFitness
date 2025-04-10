from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):  # Custom User Model
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    FITNESS_LEVELS = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')]
    GOALS = [('Weight Loss', 'Weight Loss'), ('Muscle Gain', 'Muscle Gain')]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVELS, null=True, blank=True)
    goal = models.CharField(max_length=20, choices=GOALS, null=True, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):  # Add this class definition
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
    
class Workout(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    gif_url = models.URLField()
    youtube_link = models.URLField()

    def __str__(self):
        return self.name
