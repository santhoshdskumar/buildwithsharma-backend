"""
Groq AI service for generating blog posts
"""
import os
from groq import Groq
from django.conf import settings
from datetime import datetime
import re

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class GroqAIService:
    """Service for interacting with Groq AI to generate blog content"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'GROQ_API_KEY', os.getenv('GROQ_API_KEY'))
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in settings or environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
    
    def generate_blog_post(self, topic=None, category=None):
        """
        Generate a blog post using Groq AI
        
        Args:
            topic: Optional topic for the blog post. If None, AI will choose a relevant topic.
            category: Optional category (React, Django, AWS, etc.)
        
        Returns:
            dict with title, excerpt, content, category, read_time
        """
        # Define categories and topics
        categories = ['React', 'Django', 'AWS', 'DevOps', 'Frontend', 'Backend', 'Mobile', 'Cloud', 'JavaScript', 'Python']
        
        if not category:
            # Select a category based on day of week for variety
            day_of_week = datetime.now().weekday()
            category = categories[day_of_week % len(categories)]
        
        if not topic:
            # Generate topic based on category
            topic_prompts = {
                'React': 'modern React development, performance optimization, or best practices',
                'Django': 'Django REST API, database optimization, or deployment strategies',
                'AWS': 'cloud architecture, AWS services, or infrastructure as code',
                'DevOps': 'CI/CD pipelines, containerization, or automation',
                'Frontend': 'user experience, responsive design, or frontend frameworks',
                'Backend': 'API design, server architecture, or database management',
                'Mobile': 'mobile app development, cross-platform solutions, or mobile UX',
                'Cloud': 'cloud computing, scalability, or cloud-native applications',
                'JavaScript': 'JavaScript features, ES6+, or modern JavaScript patterns',
                'Python': 'Python programming, best practices, or Python libraries'
            }
            topic = topic_prompts.get(category, 'software development and best practices')
        
        # Create the prompt for Groq AI
        system_prompt = """You are an expert technical writer specializing in software development. 
        Write comprehensive, well-structured blog posts that are informative, engaging, and practical.
        Your posts should include:
        - Clear explanations with detailed context and background
        - Multiple code examples with detailed explanations and comments
        - Best practices and common pitfalls with solutions
        - Real-world applications and use cases with examples
        - Actionable insights, tips, and tricks
        - Step-by-step guides with screenshots descriptions
        - Performance considerations and optimization techniques
        - Security best practices when relevant
        - Troubleshooting guides for common issues
        - Comparison with alternatives when applicable
        - Future trends and considerations
        
        Format your response as a detailed blog post with proper HTML formatting using <h2>, <h3>, <p>, <ul>, <li>, <ol>, <pre><code>, <strong>, <em>, <blockquote> tags.
        Make the content comprehensive, detailed, and educational (2000-3500 words)."""
        
        user_prompt = f"""Write a comprehensive, highly detailed blog post about {topic} in the {category} category.
        
        The blog post must include:
        1. An engaging, specific title (max 100 characters) that clearly indicates the topic
        2. A compelling excerpt (4-5 sentences, max 300 characters) that summarizes all key points and benefits
        3. Well-structured content with at least 8-10 major sections:
           - **Introduction**: Context, why this topic matters, what readers will learn (200-300 words)
           - **Understanding the Basics**: Core concepts, terminology, fundamentals explained in detail (300-400 words)
           - **Deep Dive**: Advanced concepts, how it works internally, technical details (400-500 words)
           - **Practical Examples**: Multiple real-world code examples with:
             * Complete, working code snippets
             * Detailed comments explaining each part
             * Different scenarios and use cases
             * Before/after comparisons (500-700 words)
           - **Best Practices**: Industry standards, recommended approaches, do's and don'ts (300-400 words)
           - **Common Mistakes**: Real mistakes developers make, why they happen, how to avoid them (300-400 words)
           - **Performance Optimization**: Tips for improving performance, benchmarks, optimization techniques (300-400 words)
           - **Real-World Use Cases**: Actual projects, case studies, when to use this approach (300-400 words)
           - **Troubleshooting**: Common issues, debugging tips, solutions to frequent problems (200-300 words)
           - **Conclusion**: Summary of key takeaways, next steps, additional resources (200-300 words)
        4. Include at least 5-7 complete code examples with:
           * Full working code (not snippets)
           * Detailed inline comments
           * Explanation of what each part does
           * Expected output or results
        5. Use proper HTML formatting:
           * <h2> for main sections
           * <h3> for subsections
           * <p> for paragraphs
           * <ul> and <ol> for lists
           * <pre><code> for code blocks with language specification
           * <strong> for emphasis
           * <em> for italics
           * <blockquote> for important notes
        6. Include practical tips, tricks, and pro tips throughout
        7. Cover both beginner-friendly explanations and advanced techniques
        8. Add comparison tables or lists where relevant
        9. Include "What to Remember" callout boxes
        10. Make it actionable - readers should be able to implement immediately
        
        Make the content extremely detailed, comprehensive, and educational. Aim for 2000-3500 words with substantial depth.
        Every section should provide real value and actionable insights.
        
        Return the response in this exact format:
        TITLE: [title here]
        EXCERPT: [excerpt here - 4-5 sentences]
        CONTENT: [full detailed HTML formatted content here with all sections]"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=6000,  # Increased for highly detailed content (2000-3500 words)
            )
            
            content = response.choices[0].message.content
            
            # Parse the response
            blog_data = self._parse_ai_response(content, category)
            
            return blog_data
            
        except Exception as e:
            print(f"Error generating blog post with Groq AI: {str(e)}")
            raise
    
    def _parse_ai_response(self, content, category):
        """Parse the AI response into structured blog post data"""
        # Extract title
        title_match = re.search(r'TITLE:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "AI Generated Blog Post"
        
        # Extract excerpt (now longer - 4-5 sentences)
        # Look for EXCERPT: followed by content until CONTENT: or end
        excerpt_match = re.search(r'EXCERPT:\s*(.+?)(?:\n\s*CONTENT:|$)', content, re.IGNORECASE | re.DOTALL)
        excerpt = excerpt_match.group(1).strip() if excerpt_match else "An informative blog post about software development."
        
        # Extract content - look for CONTENT: and take everything after it
        content_match = re.search(r'CONTENT:\s*(.+)$', content, re.DOTALL | re.IGNORECASE)
        blog_content = content_match.group(1).strip() if content_match else None
        
        # If content wasn't found with CONTENT: marker, try alternative patterns
        if not blog_content or len(blog_content) < 100:
            # Try to find content after EXCERPT
            if excerpt_match:
                content_after_excerpt = content.split('EXCERPT:', 1)[-1] if 'EXCERPT:' in content else content
                content_after_excerpt = content_after_excerpt.split('CONTENT:', 1)[-1] if 'CONTENT:' in content_after_excerpt else content_after_excerpt
                # Remove excerpt part
                if excerpt_match.group(1) in content_after_excerpt:
                    content_after_excerpt = content_after_excerpt.split(excerpt_match.group(1), 1)[-1]
                blog_content = content_after_excerpt.strip()
            
            # If still no content, use everything after title and excerpt
            if not blog_content or len(blog_content) < 100:
                lines = content.split('\n')
                # Skip title and excerpt lines
                start_idx = 0
                for i, line in enumerate(lines):
                    if 'CONTENT:' in line.upper() or (i > 2 and line.strip() and not line.strip().startswith('TITLE:') and not line.strip().startswith('EXCERPT:')):
                        start_idx = i + 1 if 'CONTENT:' in line.upper() else i
                        break
                blog_content = '\n'.join(lines[start_idx:]).strip() if start_idx > 0 else content
        
        # Final fallback - use the entire content if parsing failed
        if not blog_content or len(blog_content) < 100:
            # Remove title and excerpt if they're at the start
            cleaned_content = content
            if title_match:
                cleaned_content = cleaned_content.replace(title_match.group(0), '', 1)
            if excerpt_match:
                cleaned_content = cleaned_content.replace(excerpt_match.group(0), '', 1)
            blog_content = cleaned_content.strip() if cleaned_content.strip() else content
        
        # Calculate read time (average reading speed: 150 words per minute for technical content)
        word_count = len(blog_content.split())
        read_time_minutes = max(1, round(word_count / 150))  # Slower for detailed technical content
        read_time = f"{read_time_minutes} min read"
        
        return {
            'title': title[:300],  # Ensure it fits in model field
            'excerpt': excerpt[:800],  # Increased for longer excerpts (4-5 sentences)
            'content': blog_content,
            'category': category,
            'read_time': read_time,
            'author': 'BuildWithSharma',
        }
    
    def generate_image_url(self, title, category, topic=None):
        """
        Generate technology-related image URL based on title, category, and topic
        Using Unsplash with curated technology photo IDs
        """
        # Generate a consistent index based on title hash
        title_hash = abs(hash(title)) % 100
        
        # Curated Unsplash photo IDs for technology-related images
        # These are real, verified Unsplash photo IDs for technology/programming images
        technology_photos = {
            'React': [
                '1633356122544-f134324a6cee',  # Code/Programming
                '1461749280689-9d3de136cfe4',  # Laptop with code
                '1516321318289-607f3c6c0c0b',  # Developer workspace
                '1551650975-87deedd944c3',     # Code on screen
                '1555066931-4365d14b8c6b',     # Programming
            ],
            'Django': [
                '1627398242454-45a1465c2479',  # Python code
                '1526374965320-7f61d105fbb8',  # Code editor
                '1551650975-87deedd944c3',     # Development
                '1555066931-4365d14b8c6b',     # Programming
                '1461749280689-9d3de136cfe4',  # Tech workspace
            ],
            'AWS': [
                '1544383835-bda2bc66a55d',     # Cloud infrastructure
                '1550751827-4bd374c3f58b',     # Server/Cloud
                '1558494949-ef5f4c4e5c5b',     # Technology
                '1551650975-87deedd944c3',     # Cloud computing
                '1550751827-4bd374c3f58b',     # Data center
            ],
            'DevOps': [
                '1551650975-87deedd944c3',     # Automation
                '1558494949-ef5f4c4e5c5b',     # Technology
                '1461749280689-9d3de136cfe4',  # Development
                '1555066931-4365d14b8c6b',     # CI/CD
                '1516321318289-607f3c6c0c0b',  # DevOps tools
            ],
            'Frontend': [
                '1507003211169-0a1dd7228f2d',  # Web design
                '1516321318289-607f3c6c0c0b',  # UI/UX
                '1461749280689-9d3de136cfe4',  # Frontend development
                '1633356122544-f134324a6cee',  # Web development
                '1551650975-87deedd944c3',     # Design tools
            ],
            'Backend': [
                '1627398242454-45a1465c2479',  # Server code
                '1526374965320-7f61d105fbb8',  # Backend development
                '1555066931-4365d14b8c6b',     # API development
                '1461749280689-9d3de136cfe4',  # Server architecture
                '1551650975-87deedd944c3',     # Database
            ],
            'Mobile': [
                '1551650975-87deedd944c3',     # Mobile app
                '1516321318289-607f3c6c0c0b',  # Smartphone
                '1507003211169-0a1dd7228f2d',  # Mobile development
                '1461749280689-9d3de136cfe4',  # App development
                '1555066931-4365d14b8c6b',     # Mobile UI
            ],
            'Cloud': [
                '1544383835-bda2bc66a55d',     # Cloud services
                '1550751827-4bd374c3f58b',     # Cloud infrastructure
                '1558494949-ef5f4c4e5c5b',     # Cloud computing
                '1551650975-87deedd944c3',     # Technology
                '1461749280689-9d3de136cfe4',  # Cloud architecture
            ],
            'JavaScript': [
                '1633356122544-f134324a6cee',  # JavaScript code
                '1461749280689-9d3de136cfe4',  # JS development
                '1516321318289-607f3c6c0c0b',  # Programming
                '1551650975-87deedd944c3',     # Code
                '1555066931-4365d14b8c6b',     # JavaScript
            ],
            'Python': [
                '1627398242454-45a1465c2479',  # Python code
                '1526374965320-7f61d105fbb8',  # Python programming
                '1555066931-4365d14b8c6b',     # Code editor
                '1461749280689-9d3de136cfe4',  # Development
                '1551650975-87deedd944c3',     # Python
            ],
        }
        
        # Get photos for the category
        photos = technology_photos.get(category, technology_photos['React'])
        
        # Select a photo based on title hash for consistency
        selected_photo_id = photos[title_hash % len(photos)]
        
        # Use Unsplash images API with the selected photo ID
        # Format: https://images.unsplash.com/photo-{photo_id}?w=800&h=400&fit=crop&q=80&auto=format
        return f"https://images.unsplash.com/photo-{selected_photo_id}?w=800&h=400&fit=crop&q=80&auto=format"

