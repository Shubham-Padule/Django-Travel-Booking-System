import os
import django
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TravelManager.settings')
django.setup()

User = get_user_model()

username = 'admin'
password = '123'  # 👈 Yahan apna password likho
email = 'admin@example.com'

try:
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}...")
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully!")
    else:
        print(f"Superuser '{username}' already exists.")
except Exception as e:
    print(f"Error: {e}")