from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
import time
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from drchrono.models import PatientModel
from django.conf import settings
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

@periodic_task(run_every=(crontab(minute=5,hour=0)), name="some_task1")
def some_task1():

    all_entries = PatientModel.objects.values_list('fname','email','dob','mailsent')

    date_today = time.strftime("%Y-%m-%d")
    date_today = date_today[5:]
    def_email_txt = "Heartiest Greetings & best wishes for a Sweet Person.There is no end to all the joy I'm wishing you, with all my best wishes on your Birthday.The warmest greetings come today To wish you nothing less than everything That fills your heart with special happiness again Many many happy Returns of The Day Wish you Best of Luck."
    plaintext = get_template('email.txt')
    htmly     = get_template('email.html')

    for entry in all_entries:
        dob = entry[2]
        if dob != '' and dob != None:
            dob = dob[5:]
            if dob == date_today and entry[1] != '':

                d = Context({ 'username': entry[0],'text' : def_email_txt })
                subject, from_email, to = 'Yay! Its Your Birthday!', 'vpallavi91@gmail.com', [entry[1]]
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.mixed_subtype = 'related'

                for f in ['bg.png', 'happy_01.jpg','happy_02.jpg']:
                    fp = open(settings.MEDIA_ROOT+'/'+f, 'rb')
                    msg_img = MIMEImage(fp.read())
                    fp.close()
                    msg_img.add_header('Content-ID', '<'+f+'>')
                    msg.attach(msg_img)
                msg.send()
                t = PatientModel.objects.get(fname=entry[0],lname=entry[1],dob=entry[2])
                t.mailsent = True
                t.save()
