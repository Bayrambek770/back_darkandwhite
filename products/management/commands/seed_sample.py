from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Create a sample product if none exist"

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING("Products already exist. Skipping."))
            return
        Product.objects.create(
            name="Sample CPU",
            description="A fast CPU for testing",
            price=199.99,
            brand="SampleBrand",
            category="CPU",
            stock=10,
        )
        self.stdout.write(self.style.SUCCESS("Seeded sample product."))
