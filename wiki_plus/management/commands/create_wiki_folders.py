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
        root_user = auth_models.User.objects.get(pk=1)
        root_article = wiki_models.Article.objects.get(pk=1)
        root_urlpath = wiki_models.URLPath.objects.get(pk=1)
        article_kwargs = {
            'owner': root_user,
            'group': root_article.group,
            'group_read': root_article.group_read,
            'group_write': root_article.group_write,
            'other_read': root_article.other_read,
            'other_write': False,#root_article.other_write,
        }
        for uv in (uv[0] for uv in uvs):
            create_folders(uv)
