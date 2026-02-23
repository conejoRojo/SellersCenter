from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.sellers.models import Seller
import os

class Command(BaseCommand):
    help = 'Crea usuarios y sellers iniciales para testing local.'

    def handle(self, *args, **kwargs):
        # 1. SuperUser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@sellerscenter.local', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created successfully (admin / admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # 2. Seller API Usuario
        seller_user, created = User.objects.get_or_create(
            username='seller1',
            defaults={"email": "seller1@example.com"}
        )
        if created:
            seller_user.set_password('seller123')
            seller_user.save()
            
            # The script emulation uses 'tenant-alpha-001'
            Seller.objects.create(
                user=seller_user,
                business_name="Tienda Alpha",
                tax_id="30-12345678-9",
                tenant_id="tenant-alpha-001",
                status="active"
            )
            self.stdout.write(self.style.SUCCESS('Seller 1 created successfully (Tenant ID: tenant-alpha-001)'))
        else:
            self.stdout.write(self.style.WARNING('Seller 1 already exists'))
