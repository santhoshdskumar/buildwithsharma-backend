from django.core.management.base import BaseCommand
from services.models import Service, ServiceFeature
from blog.models import BlogPost
from about.models import AboutContent, AboutHighlight
from experience.models import Experience, ExperienceAchievement
from contact.models import ContactInfo
from technologies.models import Technology
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seed initial data for BuildWithSharma backend'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Seed Services
        self.seed_services()
        
        # Seed Technologies
        self.seed_technologies()
        
        # Seed Blog Posts
        self.seed_blog_posts()
        
        # Seed About Content
        self.seed_about_content()
        
        # Seed Experience
        self.seed_experience()
        
        # Seed Contact Info
        self.seed_contact_info()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))

    def seed_services(self):
        self.stdout.write('Seeding services...')
        
        services_data = [
            {
                'title': 'Web Development',
                'description': 'Modern, responsive web applications using Django, React, and Angular',
                'icon': 'Code',
                'color': 'primary',
                'order': 0,
                'features': ['Django Backend', 'React Frontend', 'Angular SPA', 'RESTful APIs']
            },
            {
                'title': 'Landing Pages',
                'description': 'High-converting landing pages designed to maximize your business growth',
                'icon': 'Globe',
                'color': 'secondary',
                'order': 1,
                'features': ['Conversion Optimization', 'Mobile Responsive', 'SEO Friendly', 'Fast Loading']
            },
            {
                'title': 'Static Websites',
                'description': 'Fast, secure, and cost-effective static websites for your business',
                'icon': 'Database',
                'color': 'accent',
                'order': 2,
                'features': ['HTML/CSS/JS', 'JAMstack', 'CDN Delivery', 'GitHub Pages']
            },
            {
                'title': 'Email Marketing',
                'description': 'Professional email templates and automated email campaigns',
                'icon': 'Mail',
                'color': 'success',
                'order': 3,
                'features': ['Email Templates', 'Newsletter Design', 'Automation', 'A/B Testing']
            },
            {
                'title': 'WordPress Development',
                'description': 'Custom WordPress websites with themes, plugins, and optimization',
                'icon': 'Globe',
                'color': 'warning',
                'order': 4,
                'features': ['Custom Themes', 'Plugin Development', 'WooCommerce', 'Performance']
            },
            {
                'title': 'Wix Websites',
                'description': 'Professional Wix website design and development services',
                'icon': 'Globe',
                'color': 'info',
                'order': 5,
                'features': ['Custom Design', 'E-commerce Setup', 'SEO Optimization', 'Mobile Responsive']
            },
            {
                'title': 'Mobile Development',
                'description': 'Cross-platform mobile applications for iOS and Android',
                'icon': 'Smartphone',
                'color': 'primary',
                'order': 6,
                'features': ['React Native', 'Flutter', 'Native Apps', 'PWA']
            },
            {
                'title': 'Cloud & DevOps',
                'description': 'Scalable cloud solutions with AWS and automated CI/CD pipelines',
                'icon': 'Cloud',
                'color': 'secondary',
                'order': 7,
                'features': ['AWS Services', 'Docker', 'Kubernetes', 'CI/CD']
            }
        ]
        
        for service_data in services_data:
            features = service_data.pop('features')
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                for idx, feature_name in enumerate(features):
                    ServiceFeature.objects.create(
                        service=service,
                        name=feature_name,
                        order=idx
                    )
                self.stdout.write(f'  Created service: {service.title}')
            else:
                self.stdout.write(f'  Service already exists: {service.title}')

    def seed_technologies(self):
        self.stdout.write('Seeding technologies...')
        
        technologies_data = [
            {'name': 'Django', 'category': 'Backend', 'order': 0},
            {'name': 'React', 'category': 'Frontend', 'order': 1},
            {'name': 'Angular', 'category': 'Frontend', 'order': 2},
            {'name': 'WordPress', 'category': 'CMS', 'order': 3},
            {'name': 'Wix', 'category': 'Website Builder', 'order': 4},
            {'name': 'HTML/CSS/JS', 'category': 'Static Sites', 'order': 5},
            {'name': 'AWS', 'category': 'Cloud', 'order': 6},
            {'name': 'PostgreSQL', 'category': 'Database', 'order': 7},
            {'name': 'Docker', 'category': 'DevOps', 'order': 8},
            {'name': 'GitHub Actions', 'category': 'CI/CD', 'order': 9},
            {'name': 'Node.js', 'category': 'Backend', 'order': 10},
            {'name': 'Email Marketing', 'category': 'Marketing', 'order': 11},
        ]
        
        for tech_data in technologies_data:
            tech, created = Technology.objects.get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                self.stdout.write(f'  Created technology: {tech.name}')

    def seed_blog_posts(self):
        self.stdout.write('Seeding blog posts...')
        
        blog_posts_data = [
            {
                'title': 'Building Scalable React Applications with Modern Architecture',
                'excerpt': 'Learn how to structure your React applications for scalability and maintainability using modern patterns and best practices.',
                'content': '',
                'author': 'BuildWithSharma',
                'date': '2024-01-15',
                'read_time': '8 min read',
                'category': 'React',
                'image': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400&h=250&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Django REST API: Best Practices for Production',
                'excerpt': 'Discover the essential patterns and practices for building robust Django REST APIs that can handle production traffic.',
                'content': '',
                'author': 'BuildWithSharma',
                'date': '2024-01-10',
                'read_time': '12 min read',
                'category': 'Django',
                'image': 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=400&h=250&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'AWS Cloud Architecture: Designing for Scale',
                'excerpt': 'Explore cloud architecture patterns and learn how to design systems that can scale efficiently on AWS infrastructure.',
                'content': '',
                'author': 'BuildWithSharma',
                'date': '2024-01-05',
                'read_time': '15 min read',
                'category': 'AWS',
                'image': 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=400&h=250&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'CI/CD Pipelines: Automating Your Development Workflow',
                'excerpt': 'Set up automated deployment pipelines that improve your development workflow and reduce deployment risks.',
                'content': '',
                'author': 'BuildWithSharma',
                'date': '2024-01-01',
                'read_time': '10 min read',
                'category': 'DevOps',
                'image': 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=400&h=250&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Angular vs React: Choosing the Right Framework',
                'excerpt': 'A comprehensive comparison of Angular and React to help you make informed decisions for your next project.',
                'content': '',
                'author': 'BuildWithSharma',
                'date': '2023-12-28',
                'read_time': '14 min read',
                'category': 'Frontend',
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=250&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Mobile App Development: React Native vs Flutter',
                'excerpt': 'Compare React Native and Flutter for mobile app development and choose the best framework for your needs.',
                'content': '',
                'author': 'BuildWithSharma',
                'date': '2023-12-25',
                'read_time': '11 min read',
                'category': 'Mobile',
                'image': 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=400&h=250&fit=crop&crop=center',
                'featured': False
            }
        ]
        
        for post_data in blog_posts_data:
            slug = slugify(post_data['title'])
            post, created = BlogPost.objects.get_or_create(
                slug=slug,
                defaults={**post_data, 'slug': slug}
            )
            if created:
                self.stdout.write(f'  Created blog post: {post.title}')

    def seed_about_content(self):
        self.stdout.write('Seeding about content...')
        
        about_content_data = [
            {
                'section_title': 'My Story',
                'description': 'My journey in software development began in 2017 as a Junior UI Developer, where I discovered my passion for creating beautiful and functional user interfaces. Over the years, I\'ve evolved from frontend development to full-stack development, and now lead complex software projects as a Senior Software Engineer.',
                'order': 0
            },
            {
                'section_title': 'My Story',
                'description': 'Today, as a Senior Software Engineer, I specialize in architecting scalable solutions and leading development teams. My expertise spans across Django, React, Angular, AWS, and modern DevOps practices, helping businesses transform their digital presence through innovative software solutions.',
                'order': 1
            }
        ]
        
        for content_data in about_content_data:
            content, created = AboutContent.objects.get_or_create(
                section_title=content_data['section_title'],
                order=content_data['order'],
                defaults=content_data
            )
            if created:
                self.stdout.write(f'  Created about content: {content.section_title}')
        
        highlights_data = [
            {
                'title': 'Technical Expertise',
                'description': 'Proficient in React, Angular, Django, AWS, and modern web development practices',
                'icon': 'Code',
                'order': 0
            },
            {
                'title': 'Client Focus',
                'description': 'Dedicated to delivering exceptional user experiences and business value',
                'icon': 'Users',
                'order': 1
            },
            {
                'title': 'Quality Assurance',
                'description': 'Committed to writing clean, maintainable code and following best practices',
                'icon': 'Award',
                'order': 2
            },
            {
                'title': 'Continuous Learning',
                'description': 'Always exploring new technologies and improving development processes',
                'icon': 'Target',
                'order': 3
            }
        ]
        
        for highlight_data in highlights_data:
            highlight, created = AboutHighlight.objects.get_or_create(
                title=highlight_data['title'],
                defaults=highlight_data
            )
            if created:
                self.stdout.write(f'  Created highlight: {highlight.title}')

    def seed_experience(self):
        self.stdout.write('Seeding experience...')
        
        experiences_data = [
            {
                'title': 'Senior Software Engineer',
                'company': 'Current Role',
                'location': 'Remote',
                'period_start': '2024',
                'period_end': 'Present',
                'description': 'Leading complex software development projects with expertise in full-stack technologies. Architecting scalable solutions and mentoring development teams.',
                'order': 0,
                'achievements': [
                    'Leading enterprise-level software architecture',
                    'Mentoring junior and mid-level developers',
                    'Implementing advanced DevOps practices',
                    'Driving technical innovation and best practices'
                ]
            },
            {
                'title': 'Full-Stack Developer',
                'company': 'Previous Role',
                'location': 'Remote',
                'period_start': '2021',
                'period_end': '2023',
                'description': 'Developed end-to-end web applications using Django, React, Angular, and AWS. Led development teams and implemented scalable solutions for enterprise clients.',
                'order': 1,
                'achievements': [
                    'Led development of 25+ web applications',
                    'Implemented CI/CD pipelines and DevOps practices',
                    'Mentored junior developers and conducted code reviews',
                    'Reduced application deployment time by 70%'
                ]
            },
            {
                'title': 'UI Developer',
                'company': 'Previous Role',
                'location': 'Office',
                'period_start': '2019',
                'period_end': '2021',
                'description': 'Specialized in creating responsive user interfaces and improving user experience. Worked extensively with React, Angular, and modern frontend technologies.',
                'order': 2,
                'achievements': [
                    'Created responsive designs for 30+ applications',
                    'Improved user engagement by 45% through UX optimization',
                    'Implemented modern UI patterns and component libraries',
                    'Collaborated with design teams on user-centered solutions'
                ]
            },
            {
                'title': 'Junior UI Developer',
                'company': 'Previous Role',
                'location': 'Office',
                'period_start': '2017',
                'period_end': '2019',
                'description': 'Started career in web development focusing on frontend technologies. Learned modern web development practices and contributed to various projects.',
                'order': 3,
                'achievements': [
                    'Mastered HTML, CSS, and JavaScript fundamentals',
                    'Learned React and Angular frameworks',
                    'Contributed to 15+ frontend projects',
                    'Developed strong foundation in responsive design'
                ]
            }
        ]
        
        for exp_data in experiences_data:
            achievements = exp_data.pop('achievements')
            exp, created = Experience.objects.get_or_create(
                title=exp_data['title'],
                company=exp_data['company'],
                defaults=exp_data
            )
            if created:
                for idx, achievement_text in enumerate(achievements):
                    ExperienceAchievement.objects.create(
                        experience=exp,
                        text=achievement_text,
                        order=idx
                    )
                self.stdout.write(f'  Created experience: {exp.title}')

    def seed_contact_info(self):
        self.stdout.write('Seeding contact info...')
        
        contact_info, created = ContactInfo.objects.get_or_create(
            email='buildwithsharma@gmail.com',
            defaults={
                'phone': '+91 97396 16283',
                'location': 'Available Worldwide'
            }
        )
        if created:
            self.stdout.write('  Created contact info')
        else:
            self.stdout.write('  Contact info already exists')

