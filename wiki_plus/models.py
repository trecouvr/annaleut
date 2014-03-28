# -*- coding: utf8 -*-

from django.contrib.auth import models as auth_models
from django.db import transaction

from wiki import models as wiki_models


def get_or_create_folder(root_user, parent_path, path, title, article_kwargs):
    folder = get_folder(parent_path, path)
    if folder is None:
        folder = create_folder(root_user, parent_path, path, title, article_kwargs)
    return folder


def get_folder(parent_path, path):
    try:
        return wiki_models.URLPath.objects.get(parent=parent_path, slug=path)
    except wiki_models.URLPath.DoesNotExist:
        return None


def create_folder(root_user, parent_path, path, title, article_kwargs):
    try:
        newpath = wiki_models.URLPath.create_article(
            parent_path,
            path,
            title=title,
            content="[article_list depth:2]",
            user_message="",
            user=root_user,
            ip_address='localhost',
            article_kwargs=article_kwargs)
        transaction.commit()
        return newpath
    except:
        transaction.rollback()
        traceback.print_exc()


def create_folders(uv):
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
    uv_folder = get_or_create_folder(root_user, root_urlpath, uv, uv, article_kwargs)
    for exam in ('median', 'final', 'test'):
        title = "%s %s" % (uv, exam)
        get_or_create_folder(root_user, uv_folder, exam, title, article_kwargs)
