# -*- coding: utf8 -*-

import traceback

from django.contrib.auth import models as auth_models
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from wiki_plus.models import create_folders
from fileuploader import models as fileuploader_models
from wiki import models as wiki_models


class Command(BaseCommand):
    def handle(self, *args, **kw):
        # be sure there is a root
        management.call_command('sync_root')
        uvs = fileuploader_models.Upload.objects.values_list('uv').distinct()
        create_folders(uv[0] for uv in uvs)
