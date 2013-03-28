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
            #newfile = Document(docfile = request.FILES['docfile'])
            #newdoc.save()
            #return render_to_response(
            #    'response.html',
            #    {'answer' : 'Good job!'},
            #    context_instance = RequestContext(request)
            #)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = UploadForm() # An unbound form

    return render(request, 'upload.html', { 'form' : form, })

def response(request):
    pass 
