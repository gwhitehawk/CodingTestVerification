from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from codetests.models import UploadForm
from codetests.models import Document

def upload(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UploadForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid():
            newfile = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            return HttpResponseRedirect('/response/')
    else:
        form = UploadForm() # An unbound form

    return render(request, 'upload.html', { 'form' : form, })

def response(request):
    if (1 == 1):
        return render(request, 'response.html', { 'answer' : 'Good job', })
    else:
        return render(request, 'upload.html', { 'form' : UploadForm(), })
