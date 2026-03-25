#!/bin/bash
set -e

echo "=== Campus Lost & Found - Starting ==="

# Run migrations
echo "[1/4] Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "[2/4] Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

# Create superuser if not exists
echo "[3/4] Creating admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@campus.edu', 'admin123456',
        user_type='admin', real_name='系统管理员', department='信息技术中心')
    print('Admin user created: admin / admin123456')
else:
    print('Admin user already exists')
" 2>/dev/null || true

# Seed test data if database is empty
echo "[4/4] Seeding test data..."
python manage.py shell -c "
from items.models import Item
if Item.objects.count() == 0:
    import subprocess
    result = subprocess.run(['python', 'seed_data.py'], capture_output=True, text=True)
    print(result.stdout[-500:] if result.stdout else 'Seed done')
else:
    print(f'Data already exists: {Item.objects.count()} items')
" 2>/dev/null || true

echo "=== Initialization complete, starting services ==="
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
