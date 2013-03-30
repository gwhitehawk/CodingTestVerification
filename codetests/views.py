from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from codetests.models import UploadForm
import os
from jenkinsapi import jenkins
from codetests.controller import verify as controller_verify

REMOTE_HOST = "ec2-23-20-248-192.compute-1.amazonaws.com"
VERIFY_JOB = "verify-code-test"
SUBMISSION_PATH = "submissions/"

def save_file(newfile):
    if file:
        destination = open(SUBMISSION_PATH + newfile.name, 'wb+')
        for chunk in newfile.chunks():
            destination.write(chunk)
        destination.close()

def configure_jenkins():
    j = jenkins.Jenkins("http://" + REMOTE_HOST, '', '')
    j.get_jobs()
    j.create_job('empty', jenkins.EMPTY_CONFIG_XML)
    j.disable_job('empty')
    j.copy_job('empty', 'empty_copy')
    j.enable_job('empty_copy')
    j.reconfig_job('empty_copy', jenkins.RECONFIG_XML)

    j.delete_job('empty')
    j.delete_job('empty_copy')
    return j

def verify(problem_id, filename):
    #os.system("scp /tmp/%s %s:submissions/." % (filename, REMOTE_HOST))
    #configure_jenkins().build_job(VERIFY_JOB, {'PROBLEM' : problem_id, 'SOURCE' : filename})
    return controller_verify(problem_id, filename)

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = request.FILES['gzfile']
            save_file(newfile)
            result = verify(request.POST['problem_title'], 
            request.FILES['gzfile'].name)
            
            if result[0] == 0:
                return HttpResponseRedirect('/response/')
            else:
                return render(request, 'upload_again.html', 
                { 'failed': result[0], 'all': result[1], 'form' : form })
    else:
        form = UploadForm()

    return render(request, 'upload.html', { 'form' : form, })

def response(request):
    return render(request, 'response.html', {})
