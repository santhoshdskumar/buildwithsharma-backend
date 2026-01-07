# BuildWithSharma Backend API

Django REST Framework backend for BuildWithSharma website.

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Seed initial data:
```bash
python manage.py seed_data
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Services
- `GET /api/services/services/` - List all services
- `GET /api/services/services/{id}/` - Get service details

### Blog
- `GET /api/blog/posts/` - List all blog posts
- `GET /api/blog/posts/{id}/` - Get blog post details
- `GET /api/blog/posts/featured/` - Get featured post
- `GET /api/blog/posts/recent/` - Get recent posts

### About
- `GET /api/about/content/` - Get about content
- `GET /api/about/highlights/` - Get about highlights

### Experience
- `GET /api/experience/experiences/` - List all experiences
- `GET /api/experience/experiences/{id}/` - Get experience details

### Contact
- `GET /api/contact/info/current/` - Get contact information
- `POST /api/contact/submissions/` - Submit contact form

### Technologies
- `GET /api/technologies/technologies/` - List all technologies

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to manage content.

## Environment Variables

Create a `.env` file (optional):
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama-3.1-70b-versatile
```

## Daily Blog Post Generation with Groq AI

This project includes automatic blog post generation using Groq AI. See [GROQ_SETUP.md](GROQ_SETUP.md) for detailed setup instructions.

### Quick Start

1. Get your Groq API key from [Groq Console](https://console.groq.com/)
2. Set `GROQ_API_KEY` in your environment or `.env` file
3. Generate a blog post:
   ```bash
   python manage.py generate_daily_blog
   ```
4. Schedule daily generation using cron or task scheduler (see GROQ_SETUP.md)

## CORS Configuration

CORS is configured to allow requests from:
- http://localhost:3000
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:5173

Update `CORS_ALLOWED_ORIGINS` in `backend/settings.py` for production.

