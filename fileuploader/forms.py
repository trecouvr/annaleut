# -*- encoding: utf-8 -*-
"""
Forms to upload and search
"""

import datetime
import re

from django import forms
from django.conf import settings

import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton

from .models import Upload

class UploadForm(forms.ModelForm):
    """Form to upload a file"""
    class Meta:
        model = Upload
        fields = ('uv', 'exam_t', 'semester', 'year', 'file', 'arch_t')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            if len(file.name.split('.')) == 1:
                raise forms.ValidationError('Format de fichier invalide, format autorisés: %s' % ', '.join(settings.TASK_UPLOAD_FILE_TYPES))
            file_type = file.content_type.split('/')[-1]
            if file_type in settings.TASK_UPLOAD_FILE_TYPES:
                pass
            else:
                raise forms.ValidationError("'%s' n'est pas un format autorise, format autorises: %s" % (file_type, ', '.join(settings.TASK_UPLOAD_FILE_TYPES)))
        return file

    def clean_uv(self):
        uv = self.cleaned_data['uv']
        if uv:
            uv = uv.upper()
        return uv

class SearchForm(forms.Form):
    """Smart search form"""
    q = forms.CharField(max_length=500, label='search')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'q',
        )


    def clean(self):
        """clean the input to guess what the user wants"""
        data = self.cleaned_data
        q = data.get('q', '')
        q = q.upper()
        re_year_and_semester = re.compile('([PA]?)(\d{4})')
        re_semester = re.compile('(PRI)|(AUT).*')
        re_exam_type = re.compile('(MEDIAN)|(FINAL)|(TEST)')
        year = []
        semester = []
        exam_t = []
        uv = []
        for qq in q.split():
            qq = qq.strip()
            if re_year_and_semester.match(qq):
                t = re_year_and_semester.match(qq)
                if t.group(1): semester.append('PRI' if t.group(1) == 'P' else 'AUT')
                year.append(t.group(2))
            elif re_semester.match(qq):
                t = re_semester.match(qq).groups()
                semester.append(t[0] if t[0] else t[1])
            elif re_exam_type.match(qq):
                if qq == 'MEDIAN':
                    exam_t.append('M')
                elif qq == 'FINAL':
                    exam_t.append('F')
                elif qq == 'TEST':
                    exam_t.append('T1')
                    exam_t.append('T2')
                    exam_t.append('T3')
            else:
                uv.append(qq)
        data['uv'] = uv
        data['year'] = year
        data['semester'] = semester
        data['exam_t'] = exam_t
        print data
        return data

# some utility functions
def get_field(model, fieldname):
    return model._meta.get_field_by_name(fieldname)[0]
def get_choices(model, fieldname):
    return get_field(model, fieldname).choices
def get_label(model, fieldname):
    return capfirst(get_field(model, fieldname).verbose_name)


class ChoiceFilterWithBlank(django_filters.ChoiceFilter):
    """
    FilterChoice with a blank option
    """
    def __init__(self, model, name, blank=True, **kwargs):
        self.model = model
        label = kwargs.get('label', get_label(model, name))
        choices = kwargs.get('choices', get_choices(model, name))
        if blank:
            choices = (('', '---------'),) + tuple(choices)
        super(ChoiceFilterWithBlank,self).__init__(name=name,
                        label=label, choices=choices, **kwargs)


class UploadFilterForm(forms.Form):
    """Advanced search form"""
    def __init__(self, *args, **kwargs):
        super(UploadFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))
