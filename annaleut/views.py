# -*- coding: utf8 -*-

from django.contrib.auth import views as auth_views


def adminlogin(request):
    """Small tweak to allow classic django login (bypassing CAS)"""
    request.GET = request.GET.copy()
    request.GET['redirect'] = '/annaleut/admin/'
    return auth_views.login(request, template_name='admin/login.html',
                            redirect_field_name='redirect')
