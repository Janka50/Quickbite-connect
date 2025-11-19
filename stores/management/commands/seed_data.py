"""
QuickBite Connect - Seed Data Command
Creates sample data for testing
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from users.models import User, CustomerProfile, Address
from stores.models import Store, StoreCategory
from products.models import Product, ProductCategory
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🌱 Starting data seeding...'))

        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
            Product.objects.all().delete()
            Store.objects.all().delete()
            Address.objects.all().delete()
            CustomerProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            StoreCategory.objects.all().delete()
            ProductCategory.objects.all().delete()

        # Create Store Categories
        self.stdout.write('Creating store categories...')
        store_categories = []
        for cat_name in ['Grocery Store', 'Restaurant', 'Fast Food', 'Supermarket', 'Bakery', 'Cafe']:
            cat, created = StoreCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'is_active': True}
            )
            store_categories.append(cat)
            if created:
                self.stdout.write(f'  ✅ Created: {cat_name}')

        # Create Product Categories
        self.stdout.write('Creating product categories...')
        product_categories = []
        for cat_name in ['Fruits', 'Vegetables', 'Dairy', 'Bakery', 'Beverages', 'Snacks', 'Meat', 'Seafood']:
            cat, created = ProductCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'is_active': True}
            )
            product_categories.append(cat)
            if created:
                self.stdout.write(f'  ✅ Created: {cat_name}')

        # Create Store Owners
        self.stdout.write('Creating store owners...')
        store_owners = []
        for i in range(5):
            email = f'owner{i+1}@quickbite.com'
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': f'Owner{i+1}',
                    'last_name': 'Store',
                    'user_type': 'store_owner',
                    'phone_number': f'+123456789{i}',
                    'is_email_verified': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  ✅ Created owner: {email}')
            store_owners.append(user)

        # Create Customers
        self.stdout.write('Creating customers...')
        customers = []
        for i in range(10):
            email = f'customer{i+1}@test.com'
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': f'Customer{i+1}',
                    'last_name': 'Test',
                    'user_type': 'customer',
                    'phone_number': f'+198765432{i}',
                    'is_email_verified': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                # Create customer profile
                CustomerProfile.objects.get_or_create(
                    user=user,
                    defaults={'loyalty_points': random.randint(0, 1000)}
                )
                # Create address
                Address.objects.get_or_create(
                    user=user,
                    address_type='home',
                    defaults={
                        'address_line1': f'{random.randint(100, 999)} Main Street',
                        'city': 'New York',
                        'state': 'NY',
                        'postal_code': '10001',
                        'latitude': 40.7128 + random.uniform(-0.1, 0.1),
                        'longitude': -74.0060 + random.uniform(-0.1, 0.1),
                        'is_default': True
                    }
                )
                self.stdout.write(f'  ✅ Created customer: {email}')
            customers.append(user)

        # Create Stores
        self.stdout.write('Creating stores...')
        stores_data = [
            {
                'name': 'Fresh Mart Grocery',
                'description': 'Your neighborhood grocery store with fresh produce daily',
                'store_type': 'grocery',
                'category': 'Grocery Store'
            },
            {
                'name': 'Quick Bites Restaurant',
                'description': 'Delicious meals delivered hot and fresh',
                'store_type': 'restaurant',
                'category': 'Restaurant'
            },
            {
                'name': 'Speedy Burgers',
                'description': 'Fast food done right - burgers, fries, and more',
                'store_type': 'restaurant',
                'category': 'Fast Food'
            },
            {
                'name': 'SuperSave Market',
                'description': 'Everything you need under one roof',
                'store_type': 'supermarket',
                'category': 'Supermarket'
            },
            {
                'name': 'Golden Crust Bakery',
                'description': 'Fresh baked goods every morning',
                'store_type': 'grocery',
                'category': 'Bakery'
            },
        ]

        stores = []
        for idx, store_data in enumerate(stores_data):
            store, created = Store.objects.get_or_create(
                slug=slugify(store_data['name']),
                defaults={
                    'owner': store_owners[idx % len(store_owners)],
                    'name': store_data['name'],
                    'description': store_data['description'],
                    'store_type': store_data['store_type'],
                    'phone_number': f'+1555000{idx:04d}',
                    'email': f"{slugify(store_data['name'])}@quickbite.com",
                    'address_line1': f'{random.randint(100, 999)} Business Ave',
                    'city': 'New York',
                    'state': 'NY',
                    'postal_code': '10001',
                    'latitude': 40.7128 + random.uniform(-0.05, 0.05),
                    'longitude': -74.0060 + random.uniform(-0.05, 0.05),
                    'delivery_fee': Decimal(random.choice(['2.99', '3.99', '4.99'])),
                    'min_order_amount': Decimal('10.00'),
                    'status': 'approved',
                    'is_verified': True,
                    'is_open': True,
                    'average_rating': Decimal(random.uniform(4.0, 5.0)).quantize(Decimal('0.01')),
                    'total_reviews': random.randint(10, 100)
                }
            )
            if created:
                self.stdout.write(f'  ✅ Created store: {store_data["name"]}')
            stores.append(store)

        # Create Products
        self.stdout.write('Creating products...')
        products_data = [
            {'name': 'Fresh Apples', 'price': 3.99, 'category': 'Fruits'},
            {'name': 'Organic Bananas', 'price': 2.49, 'category': 'Fruits'},
            {'name': 'Tomatoes', 'price': 4.99, 'category': 'Vegetables'},
            {'name': 'Fresh Milk', 'price': 4.49, 'category': 'Dairy'},
            {'name': 'Whole Wheat Bread', 'price': 3.49, 'category': 'Bakery'},
            {'name': 'Orange Juice', 'price': 5.99, 'category': 'Beverages'},
            {'name': 'Potato Chips', 'price': 2.99, 'category': 'Snacks'},
            {'name': 'Chicken Breast', 'price': 8.99, 'category': 'Meat'},
            {'name': 'Salmon Fillet', 'price': 12.99, 'category': 'Seafood'},
            {'name': 'Greek Yogurt', 'price': 5.49, 'category': 'Dairy'},
        ]

        for store in stores:
            for product_data in products_data:
                category = ProductCategory.objects.filter(name=product_data['category']).first()
                product, created = Product.objects.get_or_create(
                    store=store,
                    slug=slugify(f"{product_data['name']}-{store.name}"),
                    defaults={
                        'name': product_data['name'],
                        'category': category,
                        'description': f"High quality {product_data['name'].lower()} from {store.name}",
                        'short_description': f"Fresh {product_data['name'].lower()}",
                        'price': Decimal(str(product_data['price'])),
                        'stock_quantity': random.randint(20, 100),
                        'is_available': True,
                        'average_rating': Decimal(random.uniform(3.5, 5.0)).quantize(Decimal('0.01')),
                        'total_reviews': random.randint(5, 50),
                        'total_sold': random.randint(10, 200)
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ {store.name}: {product_data["name"]}')

        self.stdout.write(self.style.SUCCESS('\n✨ Seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Summary:'))
        self.stdout.write(f'  - Store Categories: {StoreCategory.objects.count()}')
        self.stdout.write(f'  - Product Categories: {ProductCategory.objects.count()}')
        self.stdout.write(f'  - Users: {User.objects.count()}')
        self.stdout.write(f'  - Stores: {Store.objects.count()}')
        self.stdout.write(f'  - Products: {Product.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n🎉 Ready to test!'))