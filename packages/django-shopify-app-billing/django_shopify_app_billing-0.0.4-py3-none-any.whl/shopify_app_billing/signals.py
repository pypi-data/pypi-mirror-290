from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.apps import apps
from .models import ShopBilling


Shop = apps.get_model(settings.SHOPIFY_SHOP_MODEL)


@receiver(post_save, sender=Shop)
def create_shop_billing(sender, instance, created, **kwargs):
    if not hasattr(instance, "billing"):
        ShopBilling.objects.create(shop=instance)
