# -*- coding: utf8 -*-

from django.contrib.auth import models as auth_models
from django.core.management.base import BaseCommand, CommandError

from wiki import models as wiki_models


class Command(BaseCommand):

    TITLE = "Annaleut Wiki !!"

    CONTENT = """Bienvenue sur la plateforme collaborative des corrections des annales !!

Les correction sont rangées dans des dossiers `type d'examen` (final, médian, test, ...) eux même rangés dans des dossiers `uv` (mt91, sr03,...). Merci de respecter cette convention pour faciliter la recherche dans le wiki :)

Le forum supporte les formules en latex tel que

$$
\\begin{pmatrix}
a_1 & \\frac{a}{v} & a_3 \\\\
b_1 & b_2 & b_3 \\\\
c_1 & c_2 & c_3
\\end{pmatrix}
\\cdot
d_4
$$

ainsi que la coloration de code


    :::python
    print('coucou')

Enjoy

[article_list depth:0]
"""

    def handle(self, *args, **kw):
        root_user = auth_models.User.objects.get(pk=1)
        article = wiki_models.Article.objects.filter(pk=1).first()
        if article is None:
            # create it
            self.stdout.write("Create root article... ")
            article = wiki_models.URLPath.create_root(
                title=self.TITLE,
                content=self.CONTENT)
        else:
            self.stdout.write("Update root article... ")
        article.owner = root_user
        article.group_write = True
        article.group_read = True
        article.other_write = True
        article.other_read = True
        revision = article.current_revision
        revision.title = self.TITLE
        revision.content = self.CONTENT
        revision.locked = True
        article.save()
        revision.save()
        self.stdout.write("OK\n")
