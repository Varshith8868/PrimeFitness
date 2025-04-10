from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['gender', 'height', 'weight', 'fitness_level', 'goal']

class WorkoutForm(forms.Form):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    FITNESS_LEVELS = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')]
    GOAL_CHOICES = [('Muscle Gain', 'Muscle Gain'), ('Weight Loss', 'Weight Loss'), ('Strength', 'Strength')]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    height = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height (cm)'}))
    weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)'}))
    fitness_level = forms.ChoiceField(choices=FITNESS_LEVELS, widget=forms.Select(attrs={'class': 'form-control'}))
    goal = forms.ChoiceField(choices=GOAL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class DietPlanForm(forms.Form):
    budget = forms.FloatField(
        label="Enter Your Budget ($)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your budget'}),
    )
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# class SignUpForm(UserCreationForm):
#     gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect)
#     height = forms.FloatField()
#     weight = forms.FloatField()
#     fitness_level = forms.ChoiceField(choices=CustomUser.FITNESS_LEVELS)
#     goal = forms.ChoiceField(choices=CustomUser.GOALS)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2', 'gender', 'height', 'weight', 'fitness_level', 'goal']