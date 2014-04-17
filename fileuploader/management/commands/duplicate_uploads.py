from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from fileuploader import models


class Command(BaseCommand):
    help = 'Find duplicate uploads'

    def handle(self, *args, **options):
        self.stdout.write('Looking for duplicate uploads...')
        duplicates = models.Upload.objects.values('uv', 'semester', 'exam_t', 'year', 'arch_t').annotate(count=Count('pk')).filter(count__gt=1)
        for duplicate in duplicates:
            self.stdout.write('{count} - {uv} {exam_t} {semester} {year} {arch_t}'.format(**duplicate))
            del duplicate['count']
            uploads = models.Upload.objects.filter(**duplicate).select_related('uploader')
            for upload in uploads:
                self.stdout.write('\t#%s %s by %s' % (upload.pk, upload.uploaded_date, upload.uploader))
        self.stdout.write('Done.')
