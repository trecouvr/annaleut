# -*- coding: utf8 -*-

from django.db import transaction

from wiki import models as wiki_models
from fileuploader import models as fileuploader_models

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
