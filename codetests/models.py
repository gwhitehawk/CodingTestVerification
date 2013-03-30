from django.db import models
from django import forms

PROBLEM_CHOICES = (('problem1', 'problem1'), ('problem2', 'problem2',))

class Test(models.Model):
    # problem title
    problem_title = models.CharField(max_length=50)
    
    # test file name
    test_input = models.CharField(max_length=100)
    
    # upper bound for run time, checking efficiency
    max_duration = models.IntegerField()

class UploadForm(forms.Form):
    sender = forms.EmailField()
    problem_title = forms.ChoiceField(
        widget = forms.Select, 
        choices = PROBLEM_CHOICES)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 15}))
    gzfile = forms.FileField(
                label = 'Select a file',
                help_text = 'max. 1MB',
                # should be true but has validation issues
                required = False,
             )
