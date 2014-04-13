# -*- encoding: utf-8 -*-
"""
Forms to upload and search
"""

import re

from django import forms
from django.conf import settings

import django_filters

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
                raise forms.ValidationError(
                    'Format de fichier invalide, format autorisés: %s' % ', '.join(settings.TASK_UPLOAD_FILE_TYPES))
            file_type = file.content_type.split('/')[-1]
            if file_type in settings.TASK_UPLOAD_FILE_TYPES:
                pass
            else:
                raise forms.ValidationError("'%s' n'est pas un format autorise, format autorises: %s" % (
                    file_type, ', '.join(settings.TASK_UPLOAD_FILE_TYPES)))
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

    def clean(self):
        """clean the input to guess what the user wants"""
        data = self.cleaned_data
        q = data.get('q', '')
        q = q.upper()
        re_year_and_semester = re.compile('([PA]?)(\d{4})')
        re_semester = re.compile('(PRI)|(AUT).*')
        re_exam_type = re.compile('(MEDIAN)|(FINAL)|(TEST)')
        re_archive_type = re.compile('(EXAM)|(CORRECTION)|(CORRIGE)|(AUTRE)')
        year = []
        semester = []
        exam_t = []
        arch_t = []
        uv = []
        for qq in q.split():
            qq = qq.strip()
            if re_year_and_semester.match(qq):
                t = re_year_and_semester.match(qq)
                if t.group(1):
                    semester.append('PRI' if t.group(1) == 'P' else 'AUT')
                year.append(t.group(2))
            elif re_archive_type.match(qq):
                if qq in ('CORRECTION', 'CORRIGE'):
                    arch_t.append('C')
                elif qq == 'EXAM':
                    arch_t.append('E')
                elif qq == 'AUTRE':
                    arch_t.append('O')
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
        data['arch_t'] = arch_t
        print data
        return data
