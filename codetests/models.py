from django.db import models
from django import forms

PROBLEM_CHOICES = (('problem1', 'problem1'), ('problem2', 'problem2',))

class Problem(models.Model):
    title = models.CharField(max_length=50)
    statement = models.CharField(max_length=1000)

class Test(models.Model):
    # problem title
    problem_title = models.CharField(max_length=50)
    
    # test file name
    test_input = models.CharField(max_length=100)
    
    # upper bound for run time, checking efficiency
    max_duration = models.IntegerField()

class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    problem = models.ForeignKey('Problem')
    activated = models.DateTimeField("login activated", blank=True, null=True)
    expires = models.DateTimeField("login expires", blank=True, null=True)

class LoginForm(forms.Form):
    login = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class UploadForm(forms.Form):
    #sender = forms.EmailField()
    #problem_title = forms.ChoiceField(
    #    widget = forms.Select, 
    #    choices = PROBLEM_CHOICES)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 15}),
                              required = False)
    gzfile = forms.FileField(
                label = 'Select a file',
                help_text = 'max. 1MB',
                # should be true but has validation issues
                required = False,
             )
