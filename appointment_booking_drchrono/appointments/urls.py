from django.conf.urls import patterns, url


#TODO: add password reset form
urlpatterns = patterns('appointments.views',
    url(r'^appointment/(?P<practice_id>\d+)/$', 'appointment_form', name='appointment_form'),

)