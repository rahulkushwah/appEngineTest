from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from uploads.core.models import Document
from uploads.core.forms import DocumentForm
import json
import wave
import contextlib
import getpass
import os


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        Audio_Details='Test'
        resp={}
        resp['filename']='media\\'+filename
        try:
            with contextlib.closing(wave.open(resp['filename'],'r')) as f:
                resp['frames']=frames= f.getnframes()
                resp['rate']=rate= f.getframerate()
                resp['audio_length']= frames / float(rate)
                t = json.dumps(resp)
                f = open("test.txt","a")
                f.write("\n")
                f.write(t)
                return HttpResponse("Files uploaded and saved")
        except Exception as e:
            pass
            #resp['error']=str(e)

        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'Audio_Details':resp,
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })



def get_props(req):
    pass
    """resp={}
    resp['error']=''
    resp['status']=200
    if req.method=='GET':
        filename=req.GET['filename']
        resp['req_method']='GET'
    else:
        resp['status']=501
        return HttpResponse(json.dumps(resp),content_type="application/json")
    resp['filename']=filename
    try:
        with contextlib.closing(wave.open(filename,'r')) as f:
            resp['frames']=frames= f.getnframes()
            resp['rate']=rate= f.getframerate()
            resp['audio_length']= frames / float(rate)
        # element = mutagen.File(filename)
        # if element:
        #   resp['audio_format_list'] = element._mimes
        #   resp['audio_size'] = element.size
        #   resp['audio_length'] = element.length
        # else:
        #     resp['Audio_error'] = "Invalid audio file."

    except Exception as e:
        resp['error']=str(e)
        resp['status']=400
    return HttpResponse(json.dumps(resp),content_type="application/json")
    """