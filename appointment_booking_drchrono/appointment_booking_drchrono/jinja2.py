from __future__ import absolute_import  # Python 2 only

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template.defaultfilters import linebreaks, date, time, timesince

from jinja2 import Environment


def field_attrs(field_inst, **kwargs):
    """Adds html attributes to django form fields"""
    for k, v in kwargs.items():
        if v is not None:
            field_inst.field.widget.attrs[k] = v
        else:
            try:
                del field_inst.field.widget.attrs[k]
            except KeyError:
                pass
    return field_inst

def environment(**options):
    environment = Environment (
        extensions = [
            'pipeline_jinja2.jinja2.ext.PipelineExtension',
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
        ],
        **options
    )
    environment.filters.update({
        'field_attrs': field_attrs,
        'linebreaks': linebreaks,
        'date': date,
        'time': time,
        'timesince': timesince,
    })
    environment.globals.update({
        'static' : staticfiles_storage.url,
        'url' : reverse,
        'is_development' : settings.DEVELOPMENT,
        'now' : timezone.now(),
        'MEDIA_URL' : settings.MEDIA_URL,
    })
    return environment
