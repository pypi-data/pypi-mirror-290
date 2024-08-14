from django.db import models
from django.conf import settings

from ..services import get_managed_pricing_plans


class ShopBilling(models.Model):

    shop = models.OneToOneField(
        settings.SHOPIFY_SHOP_MODEL,
        on_delete=models.CASCADE,
        related_name="billing",
    )

    class Meta:
        verbose_name = "Shop Billing"
        verbose_name_plural = "Shops Billing"

    def __str__(self):
        return f"billing for {self.shop}"

    @property
    def managed_pricing_plans_url(self):
        return get_managed_pricing_plans()
