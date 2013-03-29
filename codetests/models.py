from django.db import models
from django import forms

PROBLEM_CHOICES = (('problem1', 'problem1'), ('problem2', 'problem2',))

class Test(models.Model):
    # problem title
    problem_title = models.CharField(max_length=50)
    
    # path to test file
    test_input = models.CharField(max_length=100)
    
    # solution handled according to problem id.
    # could be path to a file
    solution = models.CharField(max_length=100)

    # upper bound for run time, checking efficiency
    max_duration = models.IntegerField()

class UploadForm(forms.Form):
    sender = forms.EmailField()
    problem_title = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple, 
        choices = PROBLEM_CHOICES)
    message = forms.CharField()
    gzfile = forms.FileField(
                label = 'Select a file',
                help_text = 'max. 1MB',
                # should be true but has validation issues
                required = False,
             )

    def __unicode__(self):
        return self.sender()

class Document(models.Model):
    gzfile = models.FileField(upload_to = '/tmp/')
