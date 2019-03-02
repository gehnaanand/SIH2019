from django.shortcuts import render , render_to_response
import csv, io
from django.contrib import messages
from .table import send
from django.contrib.auth.decorators import permission_required
from .models import Contact

# Create your views here.

"""def index(request):
    return render_to_response('index.html')"""

def index(request):

    data1= {'firstdata': 'First Data', 'secondata': 'Second Data'}
    data2= "Data: 2"


    context= {
        'Data1': data1,
        'Data2': data2,
        }
    return render(request, 'index.html', context)


def stats(request):

    return render_to_response('stats.html')


# for uploading csv...

"""
Try not changing the code in contact_upload, if there are any changes required, have a backup.
sending the value of the data_set variable to the web page
"""


def contact_upload(request):
    template = "stats.html"

    prompt = {
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    """data_set = csv_file.read().decode('utf-8')"""
    data_set = send(csv_file)
    a=[]
    d={}
    for data in data_set:
        d[data[0]]=data[1:]
        a.append(data[0])
    context = {'Names' : a, 'Data' : data_set,'Dict':d}

    return render(request, template, context)
