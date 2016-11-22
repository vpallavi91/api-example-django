from django.conf.urls import include, url
from django.views.generic import TemplateView
from views import intro,patients

urlpatterns = [

    url(r'^$', intro),
    url(r'^patients/$', patients),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
