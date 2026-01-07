"""
Django management command to update image URLs for existing blog posts
This fixes 404 errors by updating to the new reliable image service
"""
from django.core.management.base import BaseCommand
from blog.models import BlogPost
from blog.services import GroqAIService


class Command(BaseCommand):
    help = 'Update image URLs for existing blog posts to fix 404 errors'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all blog posts',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Update specific blog post by ID',
        )

    def handle(self, *args, **options):
        self.stdout.write('Updating blog post images...')
        
        try:
            groq_service = GroqAIService()
        except ValueError as e:
            self.stdout.write(
                self.style.ERROR(f'Groq AI configuration error: {str(e)}')
            )
            self.stdout.write(
                'Note: Image generation does not require Groq API key, but service initialization does.'
            )
            # Create a minimal service instance just for image generation
            from django.conf import settings
            import os
            class MinimalGroqService:
                def generate_image_url(self, title, category, topic=None):
                    # Use technology-related Unsplash images
                    title_hash = abs(hash(title)) % 100
                    technology_photos = {
                        'React': ['1633356122544-f134324a6cee', '1461749280689-9d3de136cfe4', '1516321318289-607f3c6c0c0b', '1551650975-87deedd944c3', '1555066931-4365d14b8c6b'],
                        'Django': ['1627398242454-45a1465c2479', '1526374965320-7f61d105fbb8', '1551650975-87deedd944c3', '1555066931-4365d14b8c6b', '1461749280689-9d3de136cfe4'],
                        'AWS': ['1544383835-bda2bc66a55d', '1550751827-4bd374c3f58b', '1558494949-ef5f4c4e5c5b', '1551650975-87deedd944c3', '1550751827-4bd374c3f58b'],
                        'DevOps': ['1551650975-87deedd944c3', '1558494949-ef5f4c4e5c5b', '1461749280689-9d3de136cfe4', '1555066931-4365d14b8c6b', '1516321318289-607f3c6c0c0b'],
                        'Frontend': ['1507003211169-0a1dd7228f2d', '1516321318289-607f3c6c0c0b', '1461749280689-9d3de136cfe4', '1633356122544-f134324a6cee', '1551650975-87deedd944c3'],
                        'Backend': ['1627398242454-45a1465c2479', '1526374965320-7f61d105fbb8', '1555066931-4365d14b8c6b', '1461749280689-9d3de136cfe4', '1551650975-87deedd944c3'],
                        'Mobile': ['1551650975-87deedd944c3', '1516321318289-607f3c6c0c0b', '1507003211169-0a1dd7228f2d', '1461749280689-9d3de136cfe4', '1555066931-4365d14b8c6b'],
                        'Cloud': ['1544383835-bda2bc66a55d', '1550751827-4bd374c3f58b', '1558494949-ef5f4c4e5c5b', '1551650975-87deedd944c3', '1461749280689-9d3de136cfe4'],
                        'JavaScript': ['1633356122544-f134324a6cee', '1461749280689-9d3de136cfe4', '1516321318289-607f3c6c0c0b', '1551650975-87deedd944c3', '1555066931-4365d14b8c6b'],
                        'Python': ['1627398242454-45a1465c2479', '1526374965320-7f61d105fbb8', '1555066931-4365d14b8c6b', '1461749280689-9d3de136cfe4', '1551650975-87deedd944c3'],
                    }
                    photos = technology_photos.get(category, technology_photos['React'])
                    selected_photo_id = photos[title_hash % len(photos)]
                    return f"https://images.unsplash.com/photo-{selected_photo_id}?w=800&h=400&fit=crop&q=80&auto=format"
            groq_service = MinimalGroqService()
        
        if options['id']:
            # Update specific post
            try:
                post = BlogPost.objects.get(id=options['id'])
                old_image = post.image
                post.image = groq_service.generate_image_url(
                    post.title,
                    post.category
                )
                post.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated image for: "{post.title}"'
                    )
                )
                self.stdout.write(f'  Old: {old_image}')
                self.stdout.write(f'  New: {post.image}')
            except BlogPost.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Blog post with ID {options["id"]} not found')
                )
        elif options['all']:
            # Update all posts
            posts = BlogPost.objects.all()
            updated_count = 0
            for post in posts:
                old_image = post.image
                post.image = groq_service.generate_image_url(
                    post.title,
                    post.category
                )
                post.save()
                updated_count += 1
                self.stdout.write(f'  Updated: "{post.title}"')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {updated_count} blog post(s)'
                )
            )
        else:
            # Update posts with empty or broken images
            posts = BlogPost.objects.filter(image__isnull=True) | BlogPost.objects.filter(image='')
            updated_count = 0
            
            for post in posts:
                post.image = groq_service.generate_image_url(
                    post.title,
                    post.category
                )
                post.save()
                updated_count += 1
                self.stdout.write(f'  Updated: "{post.title}"')
            
            if updated_count == 0:
                self.stdout.write('No blog posts with empty images found.')
                self.stdout.write('Use --all to update all posts or --id <id> for specific post.')
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully updated {updated_count} blog post(s)'
                    )
                )

