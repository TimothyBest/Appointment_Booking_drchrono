from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from collections import OrderedDict
import datetime
import urllib

from accounts.forms import PatientForm
from accounts.models import Practice
from accounts.views import SignupFormView
from appointments.forms import AppointmentInfoForm, ScheduleForm
from drchronoAPI.models import ExamRoom
from drchronoAPI.api import drchronoAPI
from utilities.views import MultipleModelFormsView


class AppointmentFormView(MultipleModelFormsView):
    form_classes = {
        'AppointmentInfoForm' : AppointmentInfoForm,
        'PatientForm' : PatientForm,
        'ScheduleForm' : ScheduleForm,
    }
    template_name='appointments/schedule_form.html'

    def dispatch(self, *args, **kwargs):
        practice_id = self.kwargs.get('practice_id', None)
        self.practice = get_object_or_404(Practice, user_id=practice_id)
        self.drchrono = drchronoAPI(self.practice)
        return super(AppointmentFormView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AppointmentFormView, self).get_context_data(**kwargs)
        # TODO: this logic is also used in appointment created. when imporved be sure to fix appoinment created as well
        number_of_days = 5
        today = datetime.date.today()
        end = today + datetime.timedelta(days=number_of_days)

        start = datetime.datetime(year=2015,month=1,day=1,hour=9)
        time_slots = []
        for half_hour in range(0, 480, 30):
            time_slots.append((start + datetime.timedelta(minutes=half_hour)).time())

        available_appointments = OrderedDict()
        for days in range(number_of_days):
            date = today + datetime.timedelta(days=days)
            available_appointments[date] = list(time_slots)

        appointments = self.drchrono.get_appointments({'date_range': "%s/%s" % (today, end)})

        for appointment in appointments:
            scheduled_time = datetime.datetime.strptime(appointment['scheduled_time'], '%Y-%m-%dT%H:%M:%S')
            # round to the nearest half hour

            scheduled_time -= datetime.timedelta(minutes=scheduled_time.minute % 30)

            duration = appointment['duration']
            try:
                available_appointments[scheduled_time.date()].remove((scheduled_time).time())
            except:
                print "%s was not found in available_appointments" % scheduled_time.date()

            for half_hour in range(0, duration, 30):
                try:
                    available_appointments[scheduled_time.date()].remove((scheduled_time + datetime.timedelta(minutes=half_hour)).time())
                except:
                    pass
        context['available_appointments'] = available_appointments
        return context

    def get_objects(self, queryset=None):
        user = None
        if self.request.user.is_authenticated() and hasattr(self.request.user, 'patient'):
            user = self.request.user.patient
        return {
            'AppointmentInfoForm' : self.practice,
            'PatientForm' : user,
            'ScheduleForm' : None,
        }

    def get_success_url(self):
        return reverse('appointment_created', kwargs={'practice_id':self.practice.user.id})

    def forms_valid(self, forms):
        patient_form = forms['PatientForm'].save(commit=False)
        appointment_details = forms['AppointmentInfoForm'].cleaned_data
        # remove ScheduleForm and just use time_slots from post
        schedule = forms['ScheduleForm'].cleaned_data

        doctor = appointment_details['doctor']
        office = appointment_details['office']

        # search for user
        patient = self.drchrono.get_patients(parameters={
            'date_of_birth':patient_form.date_of_birth,
            'first_name':patient_form.first_name,
            'last_name':patient_form.last_name,
            'gender':patient_form.gender,
        })
        if len(patient) == 0:
            self.drchrono.add_patient(doctor=doctor,
                date_of_birth=patient_form.date_of_birth,
                gender=patient_form.gender, data={
                    'first_name':patient_form.first_name,
                    'last_name':patient_form.last_name,
                    'cell_phone':patient_form.cell_phone,
                    'email':patient_form.email,
                })
            patient = self.drchrono.get_patients(parameters={
                'date_of_birth':patient_form.date_of_birth,
                'first_name':patient_form.first_name,
                'last_name':patient_form.last_name,
                'gender':patient_form.gender,
            })

        # TODO: handle multiple users in some way. Possibly prompt them for information to determin who they are
        patient = patient[0]
        # TODO: better exam room select
        self.drchrono.add_appointment(data={
            'doctor': int(doctor),
            'office': int(office),
            'exam_room': int(ExamRoom.objects.filter(user=self.practice.user,office=office).first().index),
            'patient': patient['id'],
            'scheduled_time': "%sT%s" % (schedule['appointment_date'].date(), schedule['appointment_date'].time()),
            'profile': int(appointment_details['profile']),
            'notes': self.practice.note,
        })

        try:
            patient_form.id = patient['id']
            self.request.user.patient = patient_form
            self.request.user.patient.save()
        except:
            return HttpResponseRedirect("%s?signup=Ture&%s" % (self.get_success_url(), urllib.urlencode(patient)))

        return HttpResponseRedirect(self.get_success_url())

appointment_form = AppointmentFormView.as_view()

class AppointmentCreated(SignupFormView):
    template_name='appointments/created.html'

appointment_created = AppointmentCreated.as_view()
