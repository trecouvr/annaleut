# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import datetime
import mimetypes
import os

fs = FileSystemStorage(location=settings.UPLOAD_LOCATION, base_url=settings.UPLOAD_URL)


SEMESTER_CHOICES = (
    ('AUT', 'Automne'),
    ('PRI', 'Printemps'),
)
SEMESTER_DICT_CHOICES = dict(SEMESTER_CHOICES)

EXAM_T_CHOICES = (
    ('M', 'Médian'),
    ('F', 'Final'),
    ('T1', 'Test 1'),
    ('T2', 'Test 2'),
    ('T3', 'Test 3'),
    ('O', 'Autre'),
)
EXAM_T_DICT_CHOICES = dict(EXAM_T_CHOICES)

ARCH_T_CHOICES = (
    ('E', 'Exam'),
    ('C', 'Correction'),
    ('O', 'Autre'),
)
ARCH_T_DICT_CHOICES = dict(ARCH_T_CHOICES)

def upper(s):
    return s.replace('é','e').replace('è','e').upper()

def upload_to(instance, filename):
    _,ext = filename.split('.')
    return instance.compute_filename(ext)
    
class Upload(models.Model):
    # the concerned UV
    uv = models.CharField('UV', db_index=True, max_length=8, null=False, blank=False)
    # the semester
    semester = models.CharField('semestre', db_index=True, null=False, blank=False, choices=SEMESTER_CHOICES, max_length=4)
    # the type of exam
    exam_t = models.CharField('type d\'examen', db_index=True, null=False, blank=False, choices=EXAM_T_CHOICES, max_length=4)
    # the year
    year = models.IntegerField('année', db_index=True, null=False, blank=False, validators=[
            MaxValueValidator(datetime.datetime.now().year+1),
            MinValueValidator(1980)
        ])
    # the kind of archive
    arch_t = models.CharField('type d\'archive', db_index=True, null=False, blank=False, choices=ARCH_T_CHOICES, max_length=4)
    # the uploader
    uploader = models.ForeignKey(auth_models.User)
    # the date of the upload
    uploaded_date = models.DateTimeField('date d\'upload', auto_now_add=True, db_index=True, null=False, blank=False)
    # the file
    # if there is a need to protect access to resources
    # http://wiki.nginx.org/XSendfile
    # https://djangosnippets.org/snippets/491/
    # http://stackoverflow.com/questions/1729051/django-upload-to-outside-of-media-root
    file = models.FileField(upload_to=upload_to, storage=fs, null=False, blank=False)
    # is the upload available or not
    available = models.BooleanField('disponible', default=True)
    
    class Meta:
        unique_together = ('uv', 'semester', 'exam_t', 'year', 'arch_t')
    
    def pretty_semester(self):
        return SEMESTER_DICT_CHOICES.get(self.semester, 'UNKSEMESTER')
    
    def pretty_exam_t(self):
        return EXAM_T_DICT_CHOICES.get(self.exam_t, 'UNKEXAMT')
    
    def pretty_arch_t(self):
        return ARCH_T_DICT_CHOICES.get(self.arch_t, 'UNKARCHT')
    
    def compute_filename(self, ext=None):
        s = "{uv}_{exam_t}_{semester}_{year}".format(
                    uv=self.uv,
                    exam_t=upper(self.pretty_exam_t()),
                    semester=upper(self.pretty_semester()),
                    year=self.year)
        if self.arch_t == 'C':
            s += '_correction'
        mimetypes.guess_type
        if ext:
            if not ext.startswith('.'):
                ext = '.'+ext
            s += ext
        return s
