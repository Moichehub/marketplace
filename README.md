# 🛍️ Tavero - Modern Marketplace Platform

A comprehensive Django-based marketplace platform with user authentication, product management, seller dashboard, and internationalization support.

## ✨ Features

### 🏪 **Marketplace Features**
- **Product Catalog** - Browse and search products with filtering
- **Seller Dashboard** - Complete product management for sellers
- **User Authentication** - Separate registration for buyers and sellers
- **Product Management** - Create, edit, delete products with image uploads
- **Responsive Design** - Modern UI that works on all devices
- **Internationalization** - Support for English and Ukrainian languages

### 🎨 **Design & UX**
- **Modern Interface** - Clean, professional marketplace design
- **Responsive Layout** - Optimized for desktop, tablet, and mobile
- **Interactive Elements** - Hover effects, animations, and smooth transitions
- **Accessibility** - Proper contrast, focus states, and semantic HTML

### 🔧 **Technical Features**
- **Django Framework** - Robust backend with ORM and admin interface
- **Role-Based Access** - Different permissions for buyers and sellers
- **File Uploads** - Product image management
- **Slug Generation** - SEO-friendly URLs with Unicode support
- **Pagination** - Efficient product listing with HTMX support
- **Form Validation** - Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Moichehub/marketplace.git
   cd marketplace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   - Main site: http://127.0.0.1:8000
   - Admin panel: http://127.0.0.1:8000/admin

## 📁 Project Structure

```
marketplace/
├── marketplace/          # Main Django project
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── accounts/            # User authentication app
│   ├── models.py        # Custom user model
│   ├── views.py         # Authentication views
│   ├── forms.py         # Registration forms
│   └── templates/       # Auth templates
├── products/            # Product management app
│   ├── models.py        # Product and Category models
│   ├── views.py         # Product views
│   ├── forms.py         # Product forms
│   ├── filters.py       # Product filtering
│   └── templates/       # Product templates
├── orders/              # Order management app
│   ├── models.py        # Order models
│   ├── views.py         # Order views
│   └── templates/       # Order templates
├── templates/           # Base templates
│   ├── base.html        # Main layout template
│   └── home.html        # Homepage template
├── static/              # Static files
│   └── css/
│       └── style.css    # Main stylesheet
├── media/               # User uploaded files
├── locale/              # Translation files
└── manage.py            # Django management script
```

## 🎯 Key Features Explained

### **User Authentication System**
- **Custom User Model** - Extended with seller-specific fields
- **Role-Based Registration** - Separate flows for buyers and sellers
- **Secure Authentication** - Django's built-in security features

### **Product Management**
- **CRUD Operations** - Complete product lifecycle management
- **Image Uploads** - Product image handling with validation
- **Category System** - Organized product categorization
- **Stock Management** - Inventory tracking and status

### **Seller Dashboard**
- **Product Overview** - Statistics and product listing
- **Filtering & Search** - Advanced product filtering
- **Bulk Operations** - Efficient product management
- **Status Management** - Active/inactive product control

### **Internationalization**
- **Multi-language Support** - English and Ukrainian
- **Language Switcher** - Easy language switching
- **Translated Content** - All user-facing text translated

### **Responsive Design**
- **Mobile-First** - Optimized for mobile devices
- **Flexible Layout** - Adapts to different screen sizes
- **Touch-Friendly** - Proper touch targets and interactions

## 🛠️ Development

### **Adding New Features**
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Test thoroughly
4. Commit changes: `git commit -m "Add new feature"`
5. Push to remote: `git push origin feature/new-feature`
6. Create pull request

### **Database Migrations**
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

### **Static Files**
```bash
# Collect static files
python manage.py collectstatic
```

### **Translations**
```bash
# Create translation files
python manage.py makemessages -l uk

# Compile translations
python manage.py compilemessages
```

## 🧪 Testing

### **Running Tests**
```bash
python manage.py test
```

### **Test Coverage**
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📦 Deployment

### **Production Settings**
1. Create `production.py` settings file
2. Configure database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Set `DEBUG = False`

### **Environment Variables**
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for responsive design inspiration
- All contributors and testers

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**Made with ❤️ by the Tavero Team**
