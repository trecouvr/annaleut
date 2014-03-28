# -*- coding: utf8 -*-

import traceback

from django.contrib.auth import models as auth_models
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from annaleut.models import get_or_create_folder
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
            uv_folder = get_or_create_folder(root_user, root_urlpath, uv, uv, article_kwargs)
            for exam in ('median', 'final', 'test'):
                title = "%s %s" % (uv, exam)
                get_or_create_folder(root_user, uv_folder, exam, title, article_kwargs)
