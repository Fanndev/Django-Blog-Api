import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_Backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# User Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_user(
        username='admin',
        password='admin123#',
        role='admin'
    )
    print("✅ Admin user created.")
else:
    print("ℹ️ Admin user already exists.")

# User Normal
if not User.objects.filter(username='fanndev').exists():
    User.objects.create_user(
        username='fanndev',
        password='fanndev123',
        role='user'
    )
    print("✅ Normal user created.")
else:
    print("ℹ️ Normal user already exists.")
