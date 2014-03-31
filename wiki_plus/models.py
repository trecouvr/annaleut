# -*- coding: utf8 -*-

from django.contrib.auth import models as auth_models
from django.db import transaction

from wiki import models as wiki_models


def get_or_create_folder(root_user, parent_path, path, title):
    folder = get_folder(parent_path, path)
    if folder is None:
        folder = create_folder(root_user, parent_path, path, title)
    return folder


def get_folder(parent_path, path):
    try:
        return wiki_models.URLPath.objects.get(parent=parent_path, slug=path)
    except wiki_models.URLPath.DoesNotExist:
        return None


def create_folder(root_user, parent_path, path, title):
    try:
        newpath = wiki_models.URLPath.create_article(
            parent_path,
            path,
            title=title,
            content="[article_list depth:2]",
            user_message="",
            user=root_user,
            ip_address='localhost')
        transaction.commit()
        return newpath
    except:
        transaction.rollback()
        traceback.print_exc()


def create_folders(uvs):
    root_user = auth_models.User.objects.get(pk=1)
    root_article = wiki_models.Article.objects.get(pk=1)
    root_urlpath = wiki_models.URLPath.objects.get(pk=1)
    article_kwargs = {
        'owner': root_user,
        'group': root_article.group,
        'group_read': root_article.group_read,
        'group_write': root_article.group_write,
        'other_read': root_article.other_read,
        'other_write': root_article.other_write,
    }
    folders = []
    for uv in uvs:
        uv_folder = get_or_create_folder(root_user, root_urlpath, uv, uv)
        folders.append(uv_folder.pk)
        for exam in ('median', 'final', 'test'):
            title = "%s %s" % (uv, exam)
            folder = get_or_create_folder(root_user, uv_folder, exam, title)
            folders.append(folder.pk)
    wiki_models.Article.objects.filter(pk__in=folders).update(**article_kwargs)
    wiki_models.ArticleRevision.objects.filter(article__pk__in=folders).update(locked=True)
