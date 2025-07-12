# 📰 Django Blog Application

A full-featured blog application built with Django that supports user authentication, post management, commenting system, and administrative features.

---

## 🚀 Features

### 🏠 Landing Page
- **Header Navigation**: Dynamic login/register links that change to logout when authenticated.
- **Admin Access**: Special _"Manage Blog"_ link for admin users.
- **Category Sidebar**: Browse and subscribe to categories (e.g., Sports, News, Politics).
- **Top Posts**: Latest posts sorted by publish date.
- **Pagination**: 5 posts per page with navigation.

### 👤 User Management
- **Registration**: Sign up with username, email, and password confirmation.
- **Login/Logout**: Secure and reliable authentication.
- **User Blocking**: Admin can block or unblock users.
- **Admin Promotion**: Promote regular users to admin.

### 📝 Post Management
- **Post Display**: Includes title, image, content, category, and tags.
- **Comments System**: Nested commenting with single-level replies.
- **Like/Dislike**: Rate posts. Posts are auto-deleted after 10+ dislikes.
- **Content Filtering**: Automatically censors inappropriate words.
- **Search**: Filter posts by tag or title.

### 🔧 Admin Panel
- **CRUD Operations**: Full control over posts, users, and categories.
- **User Management**: Block/unblock users from a clean dashboard.
- **Content Moderation**: Manage forbidden words.
- **Admin Dashboard**: UI inspired by AdminLTE for a modern experience.

### 📧 Email Notifications
- **Subscription Confirmations**: Users receive emails when subscribing to categories.

### 🌐 API Endpoints (Django REST Framework)
- `GET /api/posts/` - List posts  
- `POST /api/posts/` - Create a post  
- `GET /api/posts/<id>/` - Retrieve a specific post  
- `PUT /api/posts/<id>/` - Update a post  
- `DELETE /api/posts/<id>/` - Delete a post  
- `GET /api/posts/<id>/comments/` - View comments  
- `POST /api/posts/<id>/comments/` - Add a comment  

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Django REST Framework
- PostgreSQL or SQLite (depending on your setup)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-blog

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Configure and migrate the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser

6. **Run the development server**
   ```bash
   python manage.py runserver