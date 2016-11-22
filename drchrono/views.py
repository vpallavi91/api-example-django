# Create your views here.
import requests
import os
import time
from django.shortcuts import render_to_response, redirect,render
from .models import PatientModel
import datetime
from datetime import datetime


def intro(request):
    if request.user.is_authenticated() == False:
        print("not authenticated")
        return render_to_response('intro.html',{'username':''})
    else:
        instance = request.user.social_auth.get(provider='drchrono')
        username = str(instance)
        print(str(instance))
        access_token = instance.extra_data['access_token']
        headers={
        'Authorization': 'Bearer %s' % access_token,
        }


        patients = []
        patients_url = 'https://drchrono.com/api/patients'
        while patients_url:
            data = requests.get(patients_url, headers=headers).json()
            patients.extend(data['results'])
            patients_url = data['next']

        for patient in patients:
            mypatient = PatientModel()
            mypatient.fname = patient['first_name']
            mypatient.lname = patient['last_name']
            mypatient.email = patient['email']
            mypatient.dob   = patient['date_of_birth']
            mypatient.gender= patient['gender']
            mypatient.save()

        return render_to_response('intro.html',{'username':username})

def patients(request):
    all_entries = PatientModel.objects.values_list('fname','lname','email','dob').order_by('dob')
    print(type(all_entries))
    data = []
    #datetime.datetime.strptime('2011-06-09', '%Y-%m-%d')

    for entry in all_entries:
        info = []
        info.append(str(entry[0]))
        info.append(str(entry[1]))
        info.append(str(entry[2]))
        print(str(entry[3]))
        #da = datetime.datetime.strptime(str(entry[3]), "%Y-%m-%d")
        if str(entry[3]) != 'None':
            info.append(datetime.strptime(str(entry[3]), "%Y-%m-%d").strftime('%m-%d'))
            info.append(datetime.strptime(str(entry[3]), "%Y-%m-%d"))
        else:
            info.append(str(entry[3]))
        data.append(info)
    return render_to_response('patient_mgmnt.html',{'data':data,'date':datetime.now().strftime('%m-%d')})
