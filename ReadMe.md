# 🛒 QuickBite Connect

A comprehensive food and grocery delivery platform built with Django and Django REST Framework.

## 🌟 Features

### Core Functionality
- ✅ **User Management** - Customer & Store Owner authentication
- ✅ **Store Management** - Multi-store support with verification
- ✅ **Product Catalog** - Complete inventory management
- ✅ **Shopping Cart** - Session-based and user-based carts
- ✅ **Order Management** - Full order lifecycle tracking
- ✅ **Payment Integration** - Stripe payment processing
- ✅ **Reviews & Ratings** - Store and product reviews
- ✅ **Notifications** - Email, SMS, and in-app notifications
- ✅ **API Documentation** - Swagger and ReDoc

### Technical Features
- RESTful API with Django REST Framework
- PostgreSQL with PostGIS for spatial queries
- Redis caching and Celery for background tasks
- Stripe payment integration
- Twilio SMS notifications
- Comprehensive admin panel
- API versioning and throttling

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (for production)
- Redis (for caching)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Quick-bite
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed sample data (optional)**
   ```bash
   python manage.py seed_data
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **API Schema**: http://127.0.0.1:8000/api/schema/
- **API Info**: http://127.0.0.1:8000/api/
- **Health Check**: http://127.0.0.1:8000/api/health/

## 🧪 Testing

### Run API Tests
```bash
python test_full_api.py
```

### Run Unit Tests (when configured)
```bash
pytest
```

## 📁 Project Structure

```
Quick-bite/
├── config/                 # Project configuration
│   ├── settings/          # Environment-based settings
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── views.py
├── users/                 # User management app
├── stores/                # Store management app
├── products/              # Product catalog app
├── orders/                # Order management app
├── payments/              # Payment processing app
├── reviews/               # Reviews and ratings app
├── notifications/         # Notification system app
├── static/                # Static files
├── media/                 # User uploaded files
├── templates/             # HTML templates
├── tests/                 # Test files
├── manage.py
├── requirements.txt
└── README.md
```

## 🔑 Admin Panel

Access the admin panel at: http://127.0.0.1:8000/admin/

Default credentials (if using seed data):
- Email: admin@quickbite.com
- Password: (set during createsuperuser)

## 🛠️ Management Commands

### Seed Sample Data
```bash
python manage.py seed_data
```

### Clear and Reseed Data
```bash
python manage.py seed_data --clear
```

## 📊 API Endpoints

### Authentication & Users
- `POST /api/users/register/` - User registration
- `GET /api/users/profile/` - Get user profile
- `GET /api/users/addresses/` - List user addresses

### Stores
- `GET /api/stores/` - List all stores
- `GET /api/stores/<slug>/` - Store detail
- `POST /api/stores/create/` - Create store (store owners)
- `GET /api/stores/categories/` - Store categories

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<slug>/` - Product detail
- `POST /api/products/create/` - Create product
- `GET /api/products/categories/` - Product categories

### Orders & Cart
- `GET /api/orders/cart/` - View cart
- `POST /api/orders/cart/add/` - Add to cart
- `POST /api/orders/create/` - Create order
- `GET /api/orders/` - List orders
- `GET /api/orders/<order_number>/` - Order detail

### Payments
- `POST /api/payments/create-intent/` - Create payment intent
- `POST /api/payments/confirm/` - Confirm payment
- `GET /api/payments/` - Payment history

### Reviews
- `GET /api/reviews/stores/<store_id>/` - Store reviews
- `POST /api/reviews/stores/create/` - Create store review
- `GET /api/reviews/products/<product_id>/` - Product reviews
- `POST /api/reviews/products/create/` - Create product review

### Notifications
- `GET /api/notifications/` - List notifications
- `GET /api/notifications/unread-count/` - Unread count
- `POST /api/notifications/<id>/read/` - Mark as read
- `GET /api/notifications/preferences/` - Notification preferences

## 🔒 Environment Variables

Key environment variables (see `.env.example` for complete list):

- `DJANGO_ENVIRONMENT` - development/production
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `STRIPE_SECRET_KEY` - Stripe API key
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `GOOGLE_MAPS_API_KEY` - Google Maps API key

## 📦 Dependencies

Major dependencies:
- Django 4.2.11
- Django REST Framework 3.14.0
- PostgreSQL (psycopg2)
- Redis & Celery
- Stripe
- Twilio
- drf-spectacular (API docs)

## 🚢 Deployment

### Railway.app Deployment

1. Create Railway account
2. Install Railway CLI
3. Link project: `railway link`
4. Deploy: `railway up`

See deployment documentation for detailed instructions.

## 📝 License

This project is built as a portfolio/learning project.

## 👥 Contributors

- Abubakar Abdullahi Janka - Initial work

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- All open-source contributors

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using Django & Python**