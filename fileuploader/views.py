# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.text import capfirst
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

import django_filters
from django_filters.views import FilterView

from wiki_plus import models as wikiplus_models

from .forms import UploadForm, SearchForm
from .models import Upload


@login_required
def upload(request):
    """The upload view

    Accept GET and POST.
    On GET display the form.
    On POST, validate the form and store the file on the disk
    """
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get the upload
            upload = form.save(commit=False)
            upload.uploader = request.user
            upload.save()
            # create wiki folders
            wikiplus_models.create_folders([upload.uv])
            messages.add_message(request, messages.SUCCESS,
                '%s enregistrée, merci pour ta collaboration :)' % upload.compute_filename())
            form = UploadForm()
    else:
        form = UploadForm()
    return render(request, 'fileuploader/upload_form.html', {'form': form})


@login_required
def dl_upload(request, pk):
    """Download view,

    Files are not accessible directly, the user must be logged, more info
    available on
    http://wiki.nginx.org/XSendfile
    https://djangosnippets.org/snippets/491/
    http://stackoverflow.com/questions/1729051/django-upload-to-outside-of-media-root
    """
    u = get_object_or_404(Upload, pk=pk)
    response = HttpResponse()
    response['Content-Disposition'] = "attachment; filename={0}".format(u.file.name)
    response['X-Accel-Redirect'] = u.file.url
    return response


def smart_search(request):
    """Search page

    Accept GET, search parameter is in the `q` parameter of the GET
    request.
    """
    uploads = Upload.objects.all()
    if request.GET.get('q', None):
        form = SearchForm(request.GET)
        if form.is_valid():
            # get the upload
            data = form.cleaned_data
            uv = data['uv']
            year = data['year']
            semester = data['semester']
            exam_t = data['exam_t']
            arch_t = data['arch_t']
            qs = Upload.objects.all()
            if uv:
                qs = qs.filter(uv__in=uv)
            if semester:
                qs = qs.filter(semester__in=semester)
            if year:
                qs = qs.filter(year__in=year)
            if exam_t:
                qs = qs.filter(exam_t__in=exam_t)
            if arch_t:
                qs = qs.filter(arch_t__in=arch_t)
            uploads = qs
    else:
        form = SearchForm()
    return render(request, 'fileuploader/upload_list_smartsearch.html',
        {'form': form, 'object_list': uploads})


class ContactView(TemplateView):
    """Very simple view to display contact email"""
    template_name = "fileuploader/contact.html"

    def get_context_data(self, **kwargs):
        ctx = super(ContactView, self).get_context_data(**kwargs)
        ctx['contact_email'] = settings.CONTACT_EMAIL
        return ctx


# some utility functions
def get_field(model, fieldname):
    return model._meta.get_field_by_name(fieldname)[0]


def get_choices(model, fieldname):
    return get_field(model, fieldname).choices


class UploadFilter(django_filters.FilterSet):
    min_year = django_filters.NumberFilter(name="year", label="Année min",
                                lookup_type='gte')
    #max_year = django_filters.NumberFilter(name="year", label="Année max",
    #                            lookup_type='lte')

    class Meta:
        model = Upload
        #fields = ('uv', 'year', 'semester', 'exam_t', 'arch_t', 'uploaded_date')
        fields = ('uv', 'semester', 'exam_t', )
        order_by = ('-year', 'year', '-uploaded_date', 'uploaded_date', )

    def __init__(self, *args, **kwargs):
        super(UploadFilter, self).__init__(*args, **kwargs)
        # add blank to the choices
        self._add_blank_choice('semester')
        self._add_blank_choice('exam_t')
        #self._add_blank_choice('arch_t')

    def _add_blank_choice(self, fieldname):
        self.filters[fieldname].extra.update(
            {'choices': (('', '---------'),) + get_choices(Upload, fieldname)})


class UploadList(FilterView):
    filterset_class = UploadFilter
    template_name = 'fileuploader/upload_list_advancedsearch.html'
    queryset = Upload.objects.filter(available=True)

    def get_context_data(self, *args, **kwargs):
        data = super(UploadList, self).get_context_data(*args, **kwargs)
        data['form'] = data['filter'].form
        return data
