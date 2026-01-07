"""
Django management command to delete all blog posts
"""
from django.core.management.base import BaseCommand
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Delete all blog posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion (required to actually delete)',
        )

    def handle(self, *args, **options):
        count = BlogPost.objects.count()
        
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    f'This will delete {count} blog post(s).'
                )
            )
            self.stdout.write(
                'Use --confirm to actually delete all blog posts.'
            )
            return
        
        deleted_count, _ = BlogPost.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {deleted_count} blog post(s)'
            )
        )

