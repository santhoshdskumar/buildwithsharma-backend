"""
Django management command to generate a daily blog post using Groq AI
Run this command daily (via cron job or scheduled task) to automatically create blog posts
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from blog.models import BlogPost
from blog.services import GroqAIService
from datetime import datetime, timedelta
import traceback


class Command(BaseCommand):
    help = 'Generate a daily blog post using Groq AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Category for the blog post (React, Django, AWS, etc.)',
        )
        parser.add_argument(
            '--topic',
            type=str,
            help='Specific topic for the blog post',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force generation even if a post already exists for today',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting daily blog post generation...')
        
        try:
            # Check if a post already exists for today
            today = timezone.now().date()
            existing_post = BlogPost.objects.filter(date=today).first()
            
            if existing_post and not options['force']:
                self.stdout.write(
                    self.style.WARNING(
                        f'Blog post already exists for today: {existing_post.title}'
                    )
                )
                self.stdout.write('Use --force to generate a new post anyway.')
                return
            
            # Initialize Groq AI service
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
            
            # Generate blog post
            category = options.get('category')
            topic = options.get('topic')
            
            self.stdout.write('Generating blog post with Groq AI...')
            blog_data = groq_service.generate_blog_post(topic=topic, category=category)
            
            # Create slug from title
            slug = slugify(blog_data['title'])
            
            # Ensure slug is unique
            base_slug = slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Generate image URL with topic information
            image_url = groq_service.generate_image_url(
                blog_data['title'],
                blog_data['category'],
                topic=topic
            )
            
            # Create blog post
            blog_post = BlogPost.objects.create(
                title=blog_data['title'],
                excerpt=blog_data['excerpt'],
                content=blog_data['content'],
                author=blog_data['author'],
                date=today,
                read_time=blog_data['read_time'],
                category=blog_data['category'],
                image=image_url,
                slug=slug,
                featured=False,  # Only one featured post at a time
                is_published=True,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully generated blog post: "{blog_post.title}"'
                )
            )
            self.stdout.write(f'  Category: {blog_post.category}')
            self.stdout.write(f'  Read time: {blog_post.read_time}')
            self.stdout.write(f'  Slug: {blog_post.slug}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating blog post: {str(e)}')
            )
            self.stdout.write(traceback.format_exc())
            raise

