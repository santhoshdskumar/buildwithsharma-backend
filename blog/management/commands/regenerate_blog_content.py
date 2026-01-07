"""
Django management command to regenerate content for blog posts that are missing content
"""
from django.core.management.base import BaseCommand
from django.db import models
from blog.models import BlogPost
from blog.services import GroqAIService
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Regenerate content for blog posts that are missing content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slug',
            type=str,
            help='Regenerate content for specific blog post by slug',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Regenerate content for all posts missing content',
        )

    def handle(self, *args, **options):
        self.stdout.write('Regenerating blog post content...')
        
        try:
            groq_service = GroqAIService()
        except ValueError as e:
            self.stdout.write(
                self.style.ERROR(f'Groq AI configuration error: {str(e)}')
            )
            self.stdout.write(
                'Please set GROQ_API_KEY in your environment variables or settings.'
            )
            return
        
        if options['slug']:
            # Regenerate specific post
            try:
                post = BlogPost.objects.get(slug=options['slug'])
                self.stdout.write(f'Regenerating content for: "{post.title}"')
                
                blog_data = groq_service.generate_blog_post(
                    topic=None,
                    category=post.category
                )
                
                post.content = blog_data['content']
                post.excerpt = blog_data['excerpt']
                post.read_time = blog_data['read_time']
                post.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully regenerated content for: "{post.title}"'
                    )
                )
                self.stdout.write(f'  Content length: {len(post.content)} characters')
                self.stdout.write(f'  Read time: {post.read_time}')
            except BlogPost.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Blog post with slug "{options["slug"]}" not found')
                )
        elif options['all']:
            # Regenerate all posts missing content
            posts = BlogPost.objects.filter(
                models.Q(content__isnull=True) | 
                models.Q(content='')
            )
            # Filter posts with very short content (less than 500 chars)
            posts = [p for p in posts if not p.content or len(p.content) < 500]
            
            updated_count = 0
            for post in posts:
                self.stdout.write(f'Regenerating content for: "{post.title}"')
                
                try:
                    blog_data = groq_service.generate_blog_post(
                        topic=None,
                        category=post.category
                    )
                    
                    post.content = blog_data['content']
                    post.excerpt = blog_data['excerpt']
                    post.read_time = blog_data['read_time']
                    post.save()
                    
                    updated_count += 1
                    self.stdout.write(f'  [OK] Updated: {len(post.content)} characters')
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  [ERROR] Error: {str(e)}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully regenerated content for {updated_count} blog post(s)'
                )
            )
        else:
            # Find posts missing content
            all_posts = BlogPost.objects.all()
            posts = [p for p in all_posts if not p.content or len(p.content) < 500]
            
            if len(posts) == 0:
                self.stdout.write('No blog posts missing content found.')
                self.stdout.write('Use --all to regenerate all posts or --slug <slug> for specific post.')
            else:
                self.stdout.write(f'Found {len(posts)} blog post(s) missing content:')
                for post in posts:
                    self.stdout.write(f'  - {post.slug}: "{post.title}"')
                self.stdout.write('\nUse --all to regenerate all or --slug <slug> for specific post.')

